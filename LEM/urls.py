from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='LEM/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'cadastro/',
        views.cadastro,
        name='cadastro'
    ),
  
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'perguntasfaq/',
        views.perguntasfaq,
        name='perguntasfaq'
    ),

    path(
        'materiais/', 
        views.materiais, 
        name='materiais'
    ),
    
    path(
        'usuarios/', 
        views.usuarios, 
        name='usuarios'
    ),
]
