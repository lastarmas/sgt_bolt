from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilUtilisateur, Projet, Tache, TimestampExecution

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ProfilUtilisateur.ROLE_CHOICES)
    telephone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profil = ProfilUtilisateur.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                telephone=self.cleaned_data['telephone']
            )
        return user

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom', 'description', 'type_travail', 'responsable', 'date_debut', 'date_fin_prevue', 'budget']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_prevue': forms.DateInput(attrs={'type': 'date'}),
        }

class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['titre', 'description', 'projet', 'assignee_a', 'statut', 'date_debut', 'date_fin_prevue', 'duree_estimee', 'progression', 'notes']
        widgets = {
            'date_debut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin_prevue': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TimestampForm(forms.ModelForm):
    class Meta:
        model = TimestampExecution
        fields = ['action', 'details']
