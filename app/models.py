from django.db import models

class Card(models.Model):
    imagem = models.ImageField()
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.titulo