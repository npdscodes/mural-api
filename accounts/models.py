from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

	SEXO_CHOICES = (
		(u'masculino', 'Masculino'),
		(u'feminino', 'Femninino'),
	)

	nome = models.CharField(max_length=100)
	sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
	email = models.EmailField(max_length=50)
	telefone = BigIntegerField(max_length=11)

class Disciplina(models.Model):
	nome = models.CharField(max_length=100)

class Turma(models.Model):
	alunos = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	professor = models.ForeignKey('Profile', on_delete=models.CASCADE)
	codigo = models.CharField(max_length=50)
	periodo = models.CharField(max_length=50)
	codigo_ativo = models.BooleanField()

class Inscricao(models.Model):
	pro = models.ForeignKey('Profile', on_delete=models.CASCADE)
	tur = models.ForeignKey('Turma', on_delete=models.CASCADE)
