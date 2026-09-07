from django.contrib import admin
from .models import (
    Card, cadastro_usuario, Localizacao_lab, Cadastro_materiais, Emprestimo,
    Visita, Duvida, FAQ, HistoricoAlteracao,
)

admin.site.register([Card, cadastro_usuario, Localizacao_lab, Cadastro_materiais, Emprestimo, Visita, Duvida, FAQ, HistoricoAlteracao])

