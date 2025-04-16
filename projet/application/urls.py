from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('inscription/', views.inscription, name='inscription'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('creer_evenement/', views.creer_evenement, name='creer_evenement'),
    path('rechercher_utilisateur/<int:evenement_id>/', views.rechercher_utilisateur, name='rechercher_utilisateur'),
    path('evenement/<int:evenement_id>/valider-presence/', views.valider_presence_evenement, name='valider_presence_evenement'),

]
