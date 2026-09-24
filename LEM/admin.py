from django.contrib import admin
from .models import (
    Card, CadastroUsuario, LocalizacaoLab, Materiais, Emprestimo,
    Visita, Duvida, FAQ, HistoricoAlteracao,
)

admin.site.register([Card, CadastroUsuario, LocalizacaoLab, Materiais, Emprestimo, Visita, Duvida, FAQ, HistoricoAlteracao])

