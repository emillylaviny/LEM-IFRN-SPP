from django.db import models

# Template - área materiais do home
class Card(models.Model):
    imagem = models.ImageField()
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.titulo
#Cadastros 
class cadastro_usuario(models.Model):
    nome_completo = models.CharField(max_length=300)
    apelido = models.CharField(max_length=300, blank=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    foto = models.ImageField(upload_to="usuarios/", blank=True, null=True)
    escola = models.CharField(max_length=150)
    declaracao_escola = models.FileField(upload_to="declaracoes/", blank=True, null=True)
    cidade_escola = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=150)
    cidade_residencia = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Localizacao_lab(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

    def __str__(self):
        return self.nome


class Cadastro_materiais(models.Model):
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
    localizacao = models.ForeignKey(Localizacao_lab, on_delete=models.SET_NULL, null=True, blank=True, related_name="materiais")
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Material"
        verbose_name_plural = "Materiais"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

####

class Emprestimo(models.Model):
    STATUS = [
        ("PENDENTE", "Pendente"),
        ("APROVADO", "Aprovado"),
        ("NEGADO", "Negado"),
        ("DEVOLVIDO", "Devolvido"),
        ("ATRASADO", "Atrasado"),
        ("CANCELADO", "Cancelado"),
    ]
    professor = models.ForeignKey(cadastro_usuario, on_delete=models.PROTECT, related_name="emprestimos")
    material = models.ForeignKey(Cadastro_materiais, on_delete=models.PROTECT, related_name="emprestimos")
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
    professor = models.ForeignKey(cadastro_usuario, on_delete=models.PROTECT, related_name="visitas")
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
    usuario = models.ForeignKey(cadastro_usuario, on_delete=models.CASCADE, related_name="duvidas")
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
        return f"Dúvida de {self.usuario.nome}"

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
    administrador = models.ForeignKey(cadastro_usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="alteracoes")
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
