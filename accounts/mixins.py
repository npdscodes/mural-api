from django.db import models


class CriacaoEAtualizacaoMixin(models.Model):
    """
    Classe abstrata que servirá de composição para os models do app accounts
    """
    class Meta:
        abstract = True

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
