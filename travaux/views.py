from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Projet, Tache, ProfilUtilisateur, TimestampExecution, TypeTravail
from .forms import InscriptionForm, ProjetForm, TacheForm, TimestampForm

def home(request):
    return render(request, 'home.html')

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie!')
            return redirect('dashboard')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

@login_required
def dashboard(request):
    user_profile = ProfilUtilisateur.objects.get(user=request.user)
    
    if user_profile.role == 'manager':
        projets = Projet.objects.filter(responsable=request.user)
        taches = Tache.objects.filter(projet__responsable=request.user)
    elif user_profile.role == 'specialiste':
        projets = Projet.objects.all()
        taches = Tache.objects.filter(assignee_a=request.user)
    else:  # conseiller
        projets = Projet.objects.all()
        taches = Tache.objects.all()

    projets_en_retard = projets.filter(date_fin_prevue__lt=timezone.now().date(), statut='en_cours')
    taches_en_retard = taches.filter(date_fin_prevue__lt=timezone.now(), statut__nom='En Cours')

    context = {
        'user_profile': user_profile,
        'projets_count': projets.count(),
        'taches_count': taches.count(),
        'projets_en_retard': projets_en_retard.count(),
        'taches_en_retard': taches_en_retard.count(),
        'projets_recent': projets.order_by('-date_creation')[:5],
        'taches_recent': taches.order_by('-date_creation')[:5],
    }
    return render(request, 'dashboard.html', context)

@login_required
def liste_projets(request):
    user_profile = ProfilUtilisateur.objects.get(user=request.user)
    
    if user_profile.role == 'manager':
        projets = Projet.objects.filter(responsable=request.user)
    else:
        projets = Projet.objects.all()

    type_travail = request.GET.get('type_travail')
    statut = request.GET.get('statut')

    if type_travail:
        projets = projets.filter(type_travail_id=type_travail)
    if statut:
        projets = projets.filter(statut=statut)

    context = {
        'projets': projets,
        'types_travail': TypeTravail.objects.all(),
    }
    return render(request, 'projets/liste.html', context)

@login_required
def detail_projet(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    taches = projet.taches.all()
    
    context = {
        'projet': projet,
        'taches': taches,
    }
    return render(request, 'projets/detail.html', context)

@login_required
@user_passes_test(lambda u: ProfilUtilisateur.objects.get(user=u).role in ['manager', 'specialiste'])
def creer_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            if ProfilUtilisateur.objects.get(user=request.user).role == 'manager':
                projet.responsable = request.user
            projet.save()
            messages.success(request, 'Projet créé avec succès!')
            return redirect('liste_projets')
    else:
        form = ProjetForm()
    
    context = {'form': form}
    return render(request, 'projets/creer.html', context)

@login_required
def liste_taches(request):
    user_profile = ProfilUtilisateur.objects.get(user=request.user)
    
    if user_profile.role == 'manager':
        taches = Tache.objects.filter(projet__responsable=request.user)
    elif user_profile.role == 'specialiste':
        taches = Tache.objects.filter(assignee_a=request.user)
    else:
        taches = Tache.objects.all()

    statut = request.GET.get('statut')
    if statut:
        taches = taches.filter(statut_id=statut)

    context = {
        'taches': taches,
    }
    return render(request, 'taches/liste.html', context)

@login_required
def detail_tache(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    timestamps = tache.timestamps.all().order_by('-timestamp')
    
    if request.method == 'POST':
        form = TimestampForm(request.POST)
        if form.is_valid():
            timestamp = form.save(commit=False)
            timestamp.tache = tache
            timestamp.utilisateur = request.user
            timestamp.save()
            messages.success(request, 'Timestamp ajouté avec succès!')
            return redirect('detail_tache', pk=pk)
    else:
        form = TimestampForm()

    context = {
        'tache': tache,
        'timestamps': timestamps,
        'form': form,
    }
    return render(request, 'taches/detail.html', context)

@login_required
@user_passes_test(lambda u: ProfilUtilisateur.objects.get(user=u).role in ['manager', 'specialiste'])
def creer_tache(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save()
            messages.success(request, 'Tâche créée avec succès!')
            return redirect('liste_taches')
    else:
        form = TacheForm()
    
    context = {'form': form}
    return render(request, 'taches/creer.html', context)

@login_required
def timestamps_execution(request):
    user_profile = ProfilUtilisateur.objects.get(user=request.user)
    
    if user_profile.role == 'manager':
        timestamps = TimestampExecution.objects.filter(tache__projet__responsable=request.user)
    elif user_profile.role == 'specialiste':
        timestamps = TimestampExecution.objects.filter(utilisateur=request.user)
    else:
        timestamps = TimestampExecution.objects.all()

    timestamps = timestamps.order_by('-timestamp')

    context = {
        'timestamps': timestamps,
    }
    return render(request, 'timestamps/liste.html', context)
