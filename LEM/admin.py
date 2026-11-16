from django.contrib import admin
from .models import (
    Card, CadastroUsuario, User, LocalizacaoLab, Materiais, Emprestimo,
    Visita, Duvida, FAQ, HistoricoAlteracao,HorarioFuncionamento,
)

admin.site.register([Card, CadastroUsuario, User, LocalizacaoLab, Materiais, Emprestimo, Visita, FAQ, HistoricoAlteracao])

@admin.register(HorarioFuncionamento)
class HorarioFuncionamentoAdmin(admin.ModelAdmin):
    list_display = ("dia", "horario", "fechado")

    @admin.display(description="Dia", ordering="dia_semana")
    def dia(self, obj):
        return obj.get_dia_semana_display()

    @admin.display(description="Horário")
    def horario(self, obj):
        return obj.texto_horario()

from django.utils import timezone

@admin.register(Duvida)
class DuvidaAdmin(admin.ModelAdmin):
    list_display = ("resumo", "autor", "status", "enviada_em")
    list_filter = ("status",)
    search_fields = ("pergunta", "usuario__first_name", "usuario__last_name", "usuario__email")
    readonly_fields = ("usuario", "pergunta", "enviada_em", "respondida_em")

    @admin.display(description="Pergunta")
    def resumo(self, obj):
        return obj.pergunta[:60] + ("..." if len(obj.pergunta) > 60 else "")

    @admin.display(description="Enviada por")
    def autor(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.email

    def save_model(self, request, obj, form, change):
        if obj.resposta and obj.status == "PENDENTE":
            obj.status = "RESPONDIDA"
        if obj.status in ("RESPONDIDA", "FAQ") and not obj.respondida_em:
            obj.respondida_em = timezone.now()
        super().save_model(request, obj, form, change)