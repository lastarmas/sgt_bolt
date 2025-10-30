from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProfilUtilisateur(models.Model):
    ROLE_CHOICES = [
        ('conseiller', 'Conseiller'),
        ('manager', 'Manager'),
        ('specialiste', 'Spécialiste'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class TypeTravail(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom

class StatutTache(models.Model):
    nom = models.CharField(max_length=50)
    couleur = models.CharField(max_length=7, default='#007bff')
    
    def __str__(self):
        return self.nom

class Projet(models.Model):
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé'),
        ('suspendu', 'Suspendu'),
    ]
    
    nom = models.CharField(max_length=200)
    description = models.TextField()
    type_travail = models.ForeignKey(TypeTravail, on_delete=models.CASCADE)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets_geres')
    date_debut = models.DateField()
    date_fin_prevue = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

class Tache(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches')
    assignee_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taches_assignees')
    statut = models.ForeignKey(StatutTache, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin_prevue = models.DateTimeField()
    date_fin_reelle = models.DateTimeField(null=True, blank=True)
    duree_estimee = models.IntegerField(help_text="Durée estimée en heures")
    progression = models.IntegerField(default=0, help_text="Progression en pourcentage")
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    def est_en_retard(self):
        return self.date_fin_prevue < timezone.now() and self.statut.nom != 'Terminé'

class TimestampExecution(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='timestamps')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tache.titre} - {self.action} - {self.timestamp}"
