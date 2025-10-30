from django.contrib import admin
from .models import Projet, Tache, TypeTravail, StatutTache, ProfilUtilisateur

@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'telephone']
    list_filter = ['role']

@admin.register(TypeTravail)
class TypeTravailAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']

@admin.register(StatutTache)
class StatutTacheAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur']

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_travail', 'responsable', 'date_debut', 'date_fin_prevue', 'statut']
    list_filter = ['type_travail', 'statut', 'responsable']

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ['titre', 'projet', 'assignee_a', 'statut', 'date_debut', 'date_fin_prevue']
    list_filter = ['statut', 'projet']
