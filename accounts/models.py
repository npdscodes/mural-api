from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.core.validators import RegexValidator

from django.conf import settings

from .mixins import CriacaoEAtualizacaoMixin


class Perfil(CriacaoEAtualizacaoMixin):
    """
    Representa as pessoas no sistema. Dados gerais pessoais. Esta classe servirá de composição para
    Professor e Aluno dentro do sistema. Relaciona-se
    com o User do django para fins de autenticação e atutorização.
    """
    telefone_validacao = RegexValidator(regex='^\(\d{2}\) 9?\d{4}-\d{4}$', message=_('O numero telefone deve ser inserido no formato (XX) 9XXXX-XXXX'))

    SEXO_CHOICES = (
        ('Masculino', _('Masculino')),
        ('Feminino', _('Femninino')),
    )

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    nome = models.CharField(_('Nome'), max_length=150)
    sexo = models.CharField(_('Sexo'), max_length=10, choices=SEXO_CHOICES, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    telefone = models.CharField(max_length=15, validators=[telefone_validacao], blank=True)
    
    def __str__(self):
        return "%s - %s" % (self.nome, self.email)


class Disciplina(CriacaoEAtualizacaoMixin):

    nome = models.CharField(_('Nome'), max_length=100)

    def __str__(self):
        return self.nome


class Turma(CriacaoEAtualizacaoMixin):

    professor = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name="minhas_turmas", blank=False)
    codigo = models.CharField(max_length=50)
    periodo = models.CharField(max_length=50)
    codigo_ativo = models.BooleanField()
    disciplina = models.ForeignKey('Disciplina', related_name="turmas", null=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return "{} - {}".format(self.disciplina.nome, self.professor.nome)


class Inscricao(CriacaoEAtualizacaoMixin):

    perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name='minhas_inscricoes')
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, related_name='alunos')

    class Meta:
        ordering = ['perfil__nome']

    def __str__(self):
        return "%s - %s" % (self.perfil, self.turma)