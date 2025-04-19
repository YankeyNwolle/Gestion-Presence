from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from datetime import datetime, time
from django.utils.timezone import make_aware

from django.contrib.auth.models import User  # Remplace par ton modèle Utilisateur si personnalisé
from django.utils.timezone import make_aware

from .models import Utilisateur 
from django.contrib import messages

#from .models import Utilisateur, Presence, Commentaire,Evenement,Departement
from .forms import UtilisateurForm, EvenementForm, DepartementForm
from .models import Utilisateur, Presence, Departement
from datetime import date
from .models import Evenement

from .models import Presence, Departement, Evenement

def home(request):
    evenements = Evenement.objects.all()  # Récupère tous les événements de la base de données
    return render(request, "home.html", {"evenements": evenements})  # Passe les événements au template

def liste_evenements(request):
    evenements = Evenement.objects.all().order_by('-date_debut')  # Trier du plus récent au plus ancien
    return render(request, "liste_evenements.html", {"evenements": evenements})


def inscription(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.departement = form.cleaned_data['departement']  # Associe la brigade choisie
            utilisateur.save()
            print(utilisateur.departement)
            return redirect('home')
    else:
        form = UtilisateurForm()

    return render(request, 'inscription.html', {'form': form})


def rechercher_utilisateur(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    query = request.GET.get('q', '').strip()
    utilisateurs = []

    if query:
        utilisateurs = Utilisateur.objects.filter(
            Q(nom__icontains=query) | Q(numero__icontains=query)
        )

    return render(request, 'recherche.html', {
        'evenement': evenement,
        'utilisateurs': utilisateurs,
        'query': query,
    })


"""  
def valider_presence_evenement(request, evenement_id):
    if request.method == 'POST':
        utilisateur_id = request.POST.get('utilisateur_id')
        evenement = get_object_or_404(Evenement, id=evenement_id)
        utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)

        Presence.objects.create(
            membre=utilisateur,
            evenement=evenement,
            date=evenement.date_debut.date(),
            statut='present'
        )
        return redirect('tableau_de_bord')

    return redirect('home')
"""


def valider_presence_evenement(request, evenement_id):
    if request.method == 'POST':
        utilisateur_id = request.POST.get('utilisateur_id')
        evenement = get_object_or_404(Evenement, id=evenement_id)
        utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)

        # Vérifier si l'utilisateur est déjà inscrit à cet événement
        presence_existante = Presence.objects.filter(membre=utilisateur, evenement=evenement).exists()

        if presence_existante:
            messages.error(request, "Vous avez déjà validé votre présence à cet événement.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))  # Revient sur la même page

        # Enregistrer la nouvelle présence
        Presence.objects.create(
            membre=utilisateur,
            evenement=evenement,
            date=evenement.date_debut.date(),
            statut='present'
        )
        messages.success(request, "Votre présence a été validée avec succès !")
        return redirect(request.META.get('HTTP_REFERER', 'home'))  #Revient sur la même page



 # Ton modèle personnalisé Utilisateur

def creer_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            evenement = form.save(commit=False)

            # Ajouter les heures fixes
            date = form.cleaned_data['date_debut']
            evenement.date_debut = make_aware(datetime.combine(date, time(14, 0)))
            evenement.date_fin = make_aware(datetime.combine(date, time(17, 0)))

            evenement.save()  # Sauvegarde avec l'image téléversée
            return redirect('home')  # Redirection après la sauvegarde
    else:
        form = EvenementForm()

    return render(request, 'creer_evenement.html', {'form': form})


# permettre l'accessibilité du tableaud de bord à l'admin

def tableau_de_bord(request):

    # Récupérer les filtres depuis la requête GET
    date_filtre = request.GET.get('date')
    departement_filtre = request.GET.get('departement')

    # Filtrer les présences validées
    presences = Presence.objects.filter(statut__in=['present', 'absent', 'excuse']).select_related('membre', 'evenement')

    if date_filtre:
        presences = presences.filter(date=date_filtre)
    if departement_filtre:
        presences = presences.filter(membre__departement_id=departement_filtre)

    # Calcul des statistiques globales
    total_present = presences.filter(statut='present').count()
    total_absent = presences.filter(statut='absent').count()
    total_excuse = presences.filter(statut='excuse').count()

    # Statistiques par département (brigade)
    # Vérifier que chaque département contient bien des membres
    stats_par_departement = (
        Departement.objects.annotate(
            total_utilisateurs=Count('utilisateurs', distinct=True),  #  Compter correctement les membres distincts
            total_presences=Count('utilisateurs__presence', filter=Q(utilisateurs__presence__statut='present')),
        ).annotate(
            total_absences=F('total_utilisateurs') - F('total_presences')  # Déduire les absents à partir du total
        ).order_by('nom_depart')
    )

# Correction du calcul global des absents
    total_absent = sum(departement.total_absences for departement in stats_par_departement if departement.total_utilisateurs > 0)




    stats_par_evenement = (
        Evenement.objects.annotate(
            total_participants=Count('presence__membre'),  # Remplace 'utilisateurs' par le bon champ
            total_presences=Count('presence', filter=Q(presence__statut='present')),
            total_excuses=Count('presence', filter=Q(presence__statut='excuse')),
        ).annotate(
            total_absences=F('total_participants') - F('total_presences')
        ).order_by('titre')
    )


    # Récupérer tous les départements pour le filtre
    departements = Departement.objects.all()

    return render(request, 'tableau_de_bord.html', {
        'presences': presences,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_excuse': total_excuse,
        'stats_par_departement': stats_par_departement,
        'stats_par_evenement': stats_par_evenement,
        'departements': departements,
    })

# détail de chaque evenement



def statistique_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)

    # Filtrer les présences de cet événement
    presences = Presence.objects.filter(evenement=evenement)

    #Récupérer TOUS les utilisateurs inscrits à l’événement (correction)
    total_inscrits = Utilisateur.objects.filter(Q(presence__evenement=evenement) | Q(departement__isnull=False)).distinct().count()

    # Calcul des statistiques spécifiques
    total_present = presences.filter(statut='present').count()
    total_excuse = presences.filter(statut='excuse').count()

    # Correction du calcul des absents
    total_absent = total_inscrits - (total_present + total_excuse)

    # Debugging (Affiche les valeurs dans la console pour vérifier)
    print(f"Total inscrits: {total_inscrits}")
    print(f"Total présents: {total_present}")
    print(f"Total excusés: {total_excuse}")
    print(f"Total absents calculé: {total_absent}")

    # Statistiques par brigade (département)
    stats_par_brigade = (
        Departement.objects.annotate(
            total_utilisateurs=Count('utilisateurs', distinct=True),
            total_presences=Count('utilisateurs__presence', filter=Q(utilisateurs__presence__statut='present', utilisateurs__presence__evenement=evenement)),
        ).annotate(
            total_absences=F('total_utilisateurs') - F('total_presences')
        ).order_by('nom_depart')
    )

    return render(request, 'statistique_evenement.html', {
        'evenement': evenement,
        'total_present': total_present,
        'total_absent': total_absent, 
        'total_excuse': total_excuse,
        'stats_par_brigade': stats_par_brigade,
    })

# modifier un evenement(seule l'administrateur peut modifier un evenement)

def modifier_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)

    if request.method == "POST":
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié avec succès !")
            return redirect('tableau_de_bord')

    else:
        form = EvenementForm(instance=evenement)

    return render(request, "modifier_evenement.html", {"form": form, "evenement": evenement})

# supprimer un utilisateur

def supprimer_utilisateur(request, utilisateur_id):
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    
    if request.method == "POST":
        utilisateur.delete()
        messages.success(request, "Utilisateur supprimé avec succès !")
        return redirect(request.META.get('HTTP_REFERER', 'tableau_de_bord'))

    return render(request, "confirmer_suppression_utilisateur.html", {"utilisateur": utilisateur})

# supprimer un departement

def supprimer_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)

    if request.method == "POST":
        departement.delete()
        messages.success(request, "Departement supprimé avec succès !")
        return redirect(request.META.get('HTTP_REFERER', 'tableau_de_bord'))

    return render(request, "confirmer_suppression_departement.html", {"departement": departement})

# ajouter un departement

def ajouter_departement(request):
    if request.method == "POST":
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Département ajouté avec succès !")
            return redirect('tableau_de_bord')

    else:
        form = DepartementForm()

    return render(request, "ajouter_departement.html", {"form": form})