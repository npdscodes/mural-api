from django.db import models


class CreationAndUpdateMixin(models.Model):
    """
    Classe abstrata que servirá de composição para os models do app accounts
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
