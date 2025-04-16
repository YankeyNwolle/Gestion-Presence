from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import datetime, time
from django.utils.timezone import make_aware

from django.contrib.auth.models import User  # Remplace par ton modèle Utilisateur si personnalisé
from django.utils.timezone import make_aware

from .models import Utilisateur 

#from .models import Utilisateur, Presence, Commentaire,Evenement,Departement
from .forms import UtilisateurForm, EvenementForm
from .models import Utilisateur, Presence, Departement
from datetime import date
from .models import Evenement

def home(request):
    evenements = Evenement.objects.all()  # Récupère tous les événements de la base de données
    return render(request, "home.html", {"evenements": evenements})  # Passe les événements au template


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


from django.db.models import Count, Q, F
from django.shortcuts import render
from .models import Presence, Departement, Evenement

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

# 🚀 Correction du calcul global des absents
    total_absent = sum(departement.total_absences for departement in stats_par_departement if departement.total_utilisateurs > 0)




    stats_par_evenement = (
        Evenement.objects.annotate(
            total_participants=Count('presence__membre'),  # ✅ Remplace 'utilisateurs' par le bon champ
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
