from django.db import models
from django.core.validators import MaxValueValidator
import datetime

# Modèle Département
class Departement(models.Model):
    nom_depart = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom_depart

# Modèle Utilisateur
class Utilisateur(models.Model):
    NOM_ROLE = (
        ('admin', 'Administrateur'),
        ('utilisateur', 'Utilisateur'),
    )

    nom = models.CharField(max_length=250)
    prenoms = models.CharField(max_length=300)
    numero = models.CharField(max_length=250)
    date_naissance = models.DateField(validators=[MaxValueValidator(datetime.date.today())])
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=NOM_ROLE, default='utilisateur')

    def __str__(self):
        return f"{self.nom} {self.prenoms}"

    def get_role_display(self):
        return dict(Utilisateur.NOM_ROLE)[self.role]

# Modèle Evenement
class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(blank=True, null=True)
    organisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})

    def __str__(self):
        return self.titre

# Modèle Presence
class Presence(models.Model):
    STATUT_PRESENCE = (
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('excuse', 'Excusé'),
    )
    membre = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    date = models.DateField()
    statut = models.CharField(max_length=10, choices=STATUT_PRESENCE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.membre.nom} - {self.evenement.titre} - {self.date}"

    def get_statut_display(self):
        return dict(Presence.STATUT_PRESENCE)[self.statut]

# Modèle Commentaire
class Commentaire(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.utilisateur.nom} sur {self.evenement.titre}"