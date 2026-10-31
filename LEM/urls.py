from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'login/', views.LoginLEMView.as_view(), 
        name='login'),

    path('logout/', 
         views.LogoutLEMView.as_view(), 
         name='logout'),

    path(
        'cadastro/',
        views.cadastro,
        name='cadastro'
    ),
]