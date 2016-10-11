
#Builtin django
from django.db import models
from django.core.exceptions import ValidationError

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

    PAI , FILHO = "PAI" , "FILHO"

    raiz           = models.BooleanField(_("É raiz ?"),default=True)
    tipo           = models.CharField(max_length=10,default=PAI,blank=False,null=False)
    conteudo       = models.TextField(_("Conteúdo"),blank=False,null=False)
    criado_em      = models.DateTimeField(auto_now_add=True)
    perfil         = models.ForeignKey(Perfil,null=False,blank=False,on_delete=models.CASCADE,related_name="meus_comentarios")
    postagem       = models.ForeignKey(Postagem,null=False,on_delete=models.CASCADE,related_name="comentarios")
    comentario_pai = models.ForeignKey('self',default=None,null=True,on_delete=models.CASCADE,related_name="respostas")

    def save(self,*args,**kwargs):

        if re.match("^\s*$",self.conteudo):
            
            raise ValidationError(
                _("Conteúdo inválido : %(conteudo)s"),
                code="Inconsistência",
                params={"conteudo":self.conteudo}
            )

        if not re.match("PAI|FILHO",self.tipo):

            raise ValidationError(
                _("Tipo inválido : %(tipo)s"),
                code="Inconsistência",
                params={"tipo":self.tipo}
            )

        super(Comentario,self).save(*args,**kwargs)

    def responder(self,comentario):

        if self.tipo == self.FILHO and self.comentario_pai:
            raise TypeError("Operação não permitida")

        resposta = Comentario.objects.create(
            raiz=False,
            tipo=self.FILHO,
            conteudo=comentario,
            perfil=self.perfil,
            postagem=self.postagem,
            comentario_pai=self
        )

        resposta.save()
        return resposta

    def __repr__(self):
        return self.conteudo
