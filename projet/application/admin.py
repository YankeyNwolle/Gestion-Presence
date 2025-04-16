from django.contrib import admin

from .models import Departement, Utilisateur,Evenement, Presence, Commentaire


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom_depart',)


# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Evenement)
admin.site.register(Presence)
admin.site.register(Commentaire)
