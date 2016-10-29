from django.db import models

from rest_framework import authentication, permissions, filters


class CriacaoEAtualizacaoMixin(models.Model):
    """
    Classe abstrata que servirá de composição para os models do app accounts
    """
    class Meta:
        abstract = True

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)


class ViewsetPadraoMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination."""

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

