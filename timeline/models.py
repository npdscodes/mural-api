
#Builtin django
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#Builtin Python
import re

#Utilidades
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

#Models
from accounts.models import Perfil


class Postagem(models.Model):

    perfil = models.ForeignKey(Perfil,related_name="postagens")


class Comentario(models.Model):

    PAI, FILHO = "PAI", "FILHO"

    validador_tipo = RegexValidator("PAI|FILHO",
                            _("Tipo inválido"),
                            code="Inconsistência"
                    )

    validador_conteudo = RegexValidator("^\s*$",
                            _("Conteúdo inválido"),
                            code="Inconsistência"
                        )

    raiz = models.BooleanField(_("É raiz ?"), default=True)
    tipo = models.CharField(max_length=10, default=PAI, blank=False, null=False, validators=[validador_tipo])
    conteudo = models.TextField(_("Conteúdo"), blank=False, null=False, validators=[validador_conteudo])
    criado_em = models.DateTimeField(auto_now_add=True)
    perfil = models.ForeignKey(Perfil, null=False, blank=False, on_delete=models.CASCADE, related_name="meus_comentarios")
    postagem = models.ForeignKey(Postagem, null=False, on_delete=models.CASCADE, related_name="comentarios")
    comentario_pai = models.ForeignKey('self', default=None, null=True, on_delete=models.CASCADE, related_name="respostas")

    def responder(self,comentario):

        resposta = Comentario.objects.create(
            raiz=False,
            tipo=self.FILHO,
            conteudo=comentario,
            perfil=self.perfil,
            postagem=self.postagem
        )

        if self.tipo == "FILHO":
            resposta.comentario_pai = self.comentario_pai
        else:
            resposta.comentario_pai = self
        
        resposta.save()
        return resposta

    def __repr__(self):
        return self.conteudo
