from django.urls import path
from . import views 


urlpatterns = [
    path("", views.home, name="home"),
    path('inscription/', views.inscription, name='inscription'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('creer_evenement/', views.creer_evenement, name='creer_evenement'),
    path('rechercher_utilisateur/<int:evenement_id>/', views.rechercher_utilisateur, name='rechercher_utilisateur'),
    path('evenement/<int:evenement_id>/valider-presence/', views.valider_presence_evenement, name='valider_presence_evenement'),
    path('statistiques/evenement/<int:evenement_id>/', views.statistique_evenement, name='statistique_evenement'),
    path("evenements/", views.liste_evenements, name="liste_evenements"),
    path("modifier_evenement/<int:evenement_id>/", views.modifier_evenement, name="modifier_evenement"),
    #path("supprimer_utilisateur/<int:utilisateur_id>/", views.supprimer_utilisateur, name="supprimer_utilisateur"),
    #path("supprimer_departement/<int:departement_id>/", views.supprimer_departement, name="supprimer_departement"),
    #path("ajouter_departement/", views.ajouter_departement, name="ajouter_departement")
]
