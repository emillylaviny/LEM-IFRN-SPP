from django.db import models

class Card(models.Model):
    imagem = models.ImageField()
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.titulo

class cadastro_usuario (models.Model):
    nome = models.CharField(max_length=300)
    apelido = models.CharField(max_length=300)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField(auto_now=True)
    foto = models.ImageField(upload_to="")
    escola = models.CharField(max_length=150)
    declaracao_escola = models.FileField()
    cidade_escola = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=150)
    cidade_residencia = models.CharField(max_length=150)
    senha = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class login (models.Model):
    usuario_cpf = models.CharField(max_length=14)
    senha = models.CharField(max_length=150)
    
class login (models.Model):
    usuario_cpf = models.CharField(max_length=14)
    senha = models.CharField(max_length=150)

class Cadastro_materiais (models.Model):
    pass
