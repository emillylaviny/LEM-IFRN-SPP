from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# Template - área materiais do home
class Card(models.Model):
    imagem = models.ImageField()
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.titulo

class Instituicao(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.nome


class User(AbstractUser):
    vinculo_profissional = models.CharField(max_length=300, blank=True)

    vinculos_profissionais = models.ManyToManyField(
        Instituicao, blank=True, related_name="profissionais"
    )

    cpf = models.CharField(max_length=14, unique=True)
    nome_completo = models.CharField(max_length=300)
    apelido = models.CharField(max_length=300, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to="usuarios/", blank=True, null=True)
    declaracao_escola = models.FileField(upload_to="declaracoes/", blank=True, null=True)
    cidade_escola = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=150)
    cidade_residencia = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo
   

    @property
    def nome_exibicao(self):
        """Nome usado em saudações: apelido, ou o primeiro nome."""
        apelido = (self.apelido or "").strip()
        if apelido:
            return apelido

        partes = (self.nome_completo or "").split()
        return partes[0] if partes else ""


#Cadastros  

class LocalizacaoLab(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

    def __str__(self):
        return self.nome


class Materiais(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    orientacao_uso = models.TextField(blank=True)
    conceito_matematico = models.CharField(max_length=150, blank=True)
    nivel = models.CharField(max_length=100, blank=True)
    series = models.CharField(max_length=150, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    imagem = models.ImageField(upload_to="materiais/", blank=True, null=True)
    localizacao = models.ForeignKey(LocalizacaoLab, on_delete=models.SET_NULL, null=True, blank=True, related_name="materiais")
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Material"
        verbose_name_plural = "Materiais"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Emprestimo(models.Model):
    STATUS = [
        ("PENDENTE", "Pendente"),
        ("APROVADO", "Aprovado"),
        ("NEGADO", "Negado"),
        ("DEVOLVIDO", "Devolvido"),
        ("ATRASADO", "Atrasado"),
        ("CANCELADO", "Cancelado"),
    ]
    professor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="emprestimos")
    material = models.ForeignKey(Materiais, on_delete=models.PROTECT, related_name="emprestimos")
    quantidade = models.PositiveIntegerField(default=1)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_retirada = models.DateField(blank=True, null=True)
    data_devolucao_prevista = models.DateField(blank=True, null=True)
    data_devolucao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDENTE")
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_solicitacao"]
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"

    def __str__(self):
        return f"{self.professor} - {self.material}"


class Visita(models.Model):
    STATUS = [
        ("PENDENTE", "Pendente"),
        ("APROVADA", "Aprovada"),
        ("NEGADA", "Negada"),
        ("REALIZADA", "Realizada"),
        ("CANCELADA", "Cancelada"),
    ]
    professor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="visitas")
    data = models.DateField()
    horario = models.TimeField()
    quantidade_visitantes = models.PositiveIntegerField(default=1)
    finalidade = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDENTE")
    observacao = models.TextField(blank=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "-horario"]
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"

    def __str__(self):
        return f"{self.professor} - {self.data} {self.horario}"

class Duvida(models.Model):
    STATUS = [
        ("PENDENTE", "Pendente"),
        ("RESPONDIDA", "Respondida"),
        ("FAQ", "Pergunta frequente"),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="duvidas")
    pergunta = models.TextField()
    resposta = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDENTE")
    enviada_em = models.DateTimeField(auto_now_add=True)
    respondida_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-enviada_em"]
        verbose_name = "Dúvida"
        verbose_name_plural = "Dúvidas"

    def __str__(self):
        return f"Dúvida de {self.usuario.get_full_name() or self.usuario.email}"

class HorarioFuncionamento(models.Model):
    DIAS = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
    ]
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS, unique=True)
    fechado = models.BooleanField(default=False, help_text="Marque se o laboratório não abre neste dia.")
    abertura_1 = models.TimeField("1º período: abre", null=True, blank=True)
    fechamento_1 = models.TimeField("1º período: fecha", null=True, blank=True)
    abertura_2 = models.TimeField("2º período: abre", null=True, blank=True)
    fechamento_2 = models.TimeField("2º período: fecha", null=True, blank=True)

    class Meta:
        ordering = ["dia_semana"]
        verbose_name = "Horário de funcionamento"
        verbose_name_plural = "Horários de funcionamento"

    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.texto_horario()}"

    def periodos(self):
        """Lista de (abre, fecha) em que o laboratório funciona neste dia."""
        if self.fechado:
            return []
        pares = [
            (self.abertura_1, self.fechamento_1),
            (self.abertura_2, self.fechamento_2),
        ]
        return [(abre, fecha) for abre, fecha in pares if abre and fecha]

    def texto_horario(self):
        periodos = self.periodos()
        if not periodos:
            return "Fechado"
        return " · ".join(f"{abre:%H:%M} – {fecha:%H:%M}" for abre, fecha in periodos)

    def esta_aberto(self, hora):
        """True se `hora` (datetime.time) está dentro de algum período."""
        return any(abre <= hora < fecha for abre, fecha in self.periodos())

    def clean(self):
        if self.fechado:
            return
        if not (self.abertura_1 and self.fechamento_1):
            raise ValidationError("Informe a abertura e o fechamento do 1º período, ou marque o dia como fechado.")
        if self.fechamento_1 <= self.abertura_1:
            raise ValidationError("No 1º período, o fechamento deve ser depois da abertura.")
        if bool(self.abertura_2) != bool(self.fechamento_2):
            raise ValidationError("Preencha abertura e fechamento do 2º período, ou deixe os dois vazios.")
        if self.abertura_2:
            if self.fechamento_2 <= self.abertura_2:
                raise ValidationError("No 2º período, o fechamento deve ser depois da abertura.")
            if self.abertura_2 < self.fechamento_1:
                raise ValidationError("O 2º período deve começar depois do fim do 1º.")

# Iniciando CRUD de perguntas fequentes

class FAQ(models.Model):
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "pergunta"]
        verbose_name = "Pergunta frequente"
        verbose_name_plural = "Perguntas frequentes"

    def __str__(self):
        return self.pergunta

class HistoricoAlteracao(models.Model):
    administrador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="alteracoes")
    acao = models.CharField(max_length=20)
    modulo = models.CharField(max_length=100)
    objeto_id = models.PositiveIntegerField(null=True, blank=True)
    descricao = models.TextField(blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_hora"]
        verbose_name = "Histórico de alteração"
        verbose_name_plural = "Histórico de alterações"

    def __str__(self):
        return f"{self.acao} - {self.modulo} - {self.data_hora:%d/%m/%Y %H:%M}"

