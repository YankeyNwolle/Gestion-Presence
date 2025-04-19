from django import forms
from .models import Utilisateur, Evenement, Departement
from django.forms.widgets import DateInput


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenoms', 'numero', 'date_naissance', 'departement', 'role']
        # un champ pour la date d'anniversaire
        widgets = {
            'date_naissance':  DateInput(attrs={'type':'date','class':'form-control','placeholder':'Date de naissance'}),
        }



class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'description', 'date_debut', 'date_fin', 'image']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date', 'format': '%d-%m-%Y'}),
        }


class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom_depart']