from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', auth_views.LoginView.as_view(template_name='connexion.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projets/<int:pk>/', views.detail_projet, name='detail_projet'),
    path('projets/creer/', views.creer_projet, name='creer_projet'),
    
    path('taches/', views.liste_taches, name='liste_taches'),
    path('taches/<int:pk>/', views.detail_tache, name='detail_tache'),
    path('taches/creer/', views.creer_tache, name='creer_tache'),
    
    path('timestamps/', views.timestamps_execution, name='timestamps_execution'),
]
