from django.contrib import admin
from .models import (
    Card, User, LocalizacaoLab, Materiais, Emprestimo,
    Visita, Duvida, FAQ, HistoricoAlteracao,
)

admin.site.register([Card, User, LocalizacaoLab, Materiais, Emprestimo, Visita, Duvida, FAQ, HistoricoAlteracao])

