
#Builtin django
from django.db import models
from django.core.validators import RegexValidator

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


#Utilidades
from django.utils.translation import ugettext_lazy as _

#Models
from accounts.models import Perfil, Inscricao, Turma


class Postagem(models.Model):

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="postagens")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE,related_name="postagens",null=False)
    postado_em = models.DateTimeField(auto_now_add=True)

    conteudo_relacionado = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=False)
    objeto = models.PositiveIntegerField()
    content_object = GenericForeignKey('conteudo_relacionado', 'objeto')

    def __repr__(self):
        return self.__dict__


class Comentario(models.Model):

    PAI, FILHO = _("PAI"), _("FILHO")

    TIPO_COMENTARIO = (
        (PAI, _("Comentário Raiz")),
        (FILHO, _("Comentário Resposta"))
    )

    validador_tipo = RegexValidator("PAI|FILHO",
                            _("Tipo inválido"),
                            code="Inconsistência"
                    )

    validador_conteudo = RegexValidator("^\s*$",
                            _("Conteúdo inválido"),
                            code="Inconsistência"
                        )

    raiz = models.BooleanField(_("É raiz ?"), default=True)
    tipo = models.CharField(max_length=10, choices=TIPO_COMENTARIO,default=PAI, blank=False, null=False, validators=[validador_tipo])
    conteudo = models.TextField(_("Conteúdo"), blank=False, null=False, validators=[validador_conteudo])
    criado_em = models.DateTimeField(auto_now_add=True)
    perfil = models.ForeignKey(Perfil, null=False, blank=False, on_delete=models.CASCADE, related_name="meus_comentarios")
    postagem = GenericRelation(Postagem,null=False, on_delete=models.CASCADE, related_name="comentarios")    
    comentario_pai = models.ForeignKey('self', default=None, null=True, on_delete=models.CASCADE, related_name="respostas")

    def responder(self, comentario):

        resposta = Comentario.objects.create(
            raiz=False,
            tipo=Comentario.FILHO,
            conteudo=comentario,
            perfil=self.perfil,
            postagem=self.postagem
        )

        if self.tipo == Comentario.FILHO:
            resposta.comentario_pai = self.comentario_pai
        else:
            resposta.comentario_pai = self
        
        resposta.save()
        return resposta

    def __repr__(self):
        return self.conteudo


# Classes de herança para Postagem

class Aviso(Postagem):
    
    mensagem = models.TextField()

    def __repr__(self):
        return self.mensagem

class Evento(Postagem):
    
    descricao = models.CharField(max_length=30, blank=False)
    horario = models.DateTimeField()
    endereco = models.ForeignKey('Localizacao', related_name='evento')

    def __repr__(self):
        return "{} - {}".format(self.descricao, self.endereco)

class Exercicio(Postagem):
    
    descricao = models.TextField()
    data_entrega = models.DateTimeField()


# Composições 

class Resposta(models.Model):

    CONCLUIDO, NAO_CONCLUIDO = True, False

    STATUS_RESPOSTA = (
        ( CONCLUIDO , _("Concluído") ),
        ( NAO_CONCLUIDO, _("Não Concluído") )
    )

    exercicio = models.ForeignKey(Exercicio, related_name="respostas")
    aluno = models.ForeignKey(Inscricao, related_name="respostas")
    link_resposta = models.URLField()
    status = models.CharField(choices=STATUS_RESPOSTA,default=NAO_CONCLUIDO,blank=False,max_length=5)

class Localizacao(models.Model):

    local = models.CharField(max_length=30, blank=False)
    rua = models.CharField(max_length=50, blank=False)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=50, blank=False)
    cidade = models.CharField(max_length=50, blank=False)
    
