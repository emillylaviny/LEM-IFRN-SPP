from django.urls import path
from . import views

urlpatterns = [
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
        'dashboard/faq/cadastrar/',
        views.faq_cadastrar,
        name='faq_cadastrar'
    ),
    path(
        'dashboard/faq/<int:id>/editar/',
        views.faq_editar,
        name='faq_editar'
    ),
    path(
        'dashboard/faq/<int:id>/excluir/',
        views.faq_excluir,
        name='faq_excluir'
    ),

    path(
        'materiais/', 
        views.materiais, 
        name='materiais'
    ),
    
    
    path(
        'materiais/novo/',
        views.novo_material,
        name='novo_material'
    ),

    path(
        'materiais/<int:material_id>/editar/',
        views.editar_material,
        name='editar_material'
    ),

    path(
        'materiais/<int:material_id>/remover/',
        views.remover_material,
        name='remover_material'
    ),
    
    path("usuarios/", views.usuarios, name="usuarios"),
    path(
    "usuarios/formulario/",
    views.form_usuario,
    name="form_usuario"
    ),
    path("usuarios/novo/", views.usuario_cadastrar, name="usuario_cadastrar"),
    path("usuarios/editar/<int:id>/", views.usuario_editar, name="usuario_editar"),
    path("usuarios/excluir/<int:id>/", views.usuario_excluir, name="usuario_excluir"),
    path('etiquetas/', 
         views.etiquetas, 
         name='etiquetas'),

]