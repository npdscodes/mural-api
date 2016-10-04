from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    """
    Representa as pessoas no sistema. Dados gerais pessoais. Esta classe servirá de composição para
    Professor e Aluno dentro do sistema. Relaciona-se
    com o User do django para fins de autenticação e atutorização.
    """

    SEXO_CHOICES = (
        ('Masculino', _('Masculino')),
        ('Feminino', _('Femninino')),
    )

    nome = models.CharField(_('Nome'), max_length=100, null=False, blank=False)
    sexo = models.CharField(_('Sexo'), max_length=10, choices=SEXO_CHOICES)
    email = models.EmailField(max_length=50)
    telefone = models.BigIntegerField()

    def __str__(self):
        return "%s - %s" % (self.nome, self.email)


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)


class Turma(models.Model):
    professor = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="minhas_turmas")
    codigo = models.CharField(max_length=50)
    periodo = models.CharField(max_length=50)
    codigo_ativo = models.BooleanField()


class Inscricao(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='minhas_inscricoes')
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, related_name='alunos')
