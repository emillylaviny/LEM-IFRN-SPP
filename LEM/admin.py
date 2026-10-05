from django.contrib import admin
from .models import (
    Card, CadastroUsuario, User, LocalizacaoLab, Materiais, Emprestimo,
    Visita, Duvida, FAQ, HistoricoAlteracao,
)

admin.site.register([Card, CadastroUsuario, User, LocalizacaoLab, Materiais, Emprestimo, Visita, Duvida, FAQ, HistoricoAlteracao])

