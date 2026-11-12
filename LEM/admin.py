from django.contrib import admin
from .models import Instituicao
from .models import (
    Card, CadastroUsuario, User, LocalizacaoLab, Materiais, Emprestimo,
    Visita, Duvida, FAQ, HistoricoAlteracao,
)

admin.site.register([Card, CadastroUsuario, User, LocalizacaoLab, Materiais, Emprestimo, Visita, Duvida, FAQ, HistoricoAlteracao])


@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('nome',)