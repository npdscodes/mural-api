from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.core.validators import RegexValidator

from django.conf import settings


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

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nome = models.CharField(_('Nome'), max_length=150)
    sexo = models.CharField(_('Sexo'), max_length=10, choices=SEXO_CHOICES, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    telefone_validator = RegexValidator(regex='^\(\d{2}\) 9?\d{4}-\d{4}$', message=_('O numero telefone deve ser inserido no formato (XX) 9XXXX-XXXX'))
    telefone = models.CharField(max_length=15, validators=[telefone_validator], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Disciplina(models.Model):

    nome = models.CharField(_('Nome'), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Turma(models.Model):

    professor = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="minhas_turmas")
    codigo = models.CharField(max_length=50)
    periodo = models.CharField(max_length=50)
    codigo_ativo = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Inscricao(models.Model):

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='minhas_inscricoes')
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, related_name='alunos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

