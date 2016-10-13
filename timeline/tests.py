from django.test import TestCase

#Excecoes
from django.core.exceptions import ValidationError
from django.db import IntegrityError

#Modelos
from .models import Comentario, Postagem
from accounts.models import Perfil

#Factory dados fake
from model_mommy import mommy

def retornar_ids(lista):
    from django.db.models.query import QuerySet

    if isinstance(lista, QuerySet):
        return list(lista.values_list("id", flat=True))

    elif isinstance(lista, list):
        return [ elemento.id for elemento in lista]

class TestModelComentarios(TestCase):

    def setUp(self):

        self.perfil = mommy.make(Perfil)
        self.postagem = mommy.make(Postagem)
        self.comentario = mommy.make(Comentario,conteudo="Comentário Pai")

    def test_comentario_deve_ser_criado_como_raiz_por_padrao(self):
        self.assertTrue(self.comentario.raiz)

    def test_deve_retornar_tipo_correto_na_criacao(self):
        self.assertEquals(self.comentario.tipo,"PAI")

    def test_deve_retornar_o_conteudo_correto_do_comentario(self):
        self.assertEquals(self.comentario.conteudo,"Comentário Pai")

    def test_deve_gerar_excecao_com_tipo_invalido_do_comentario(self):

        with self.assertRaises(ValidationError):
            comentario = mommy.make(Comentario,tipo="MAE")

            comentario.full_clean()

    def test_deve_gerar_excecao_quando_nao_houver_postagem_associada(self):

        with self.assertRaises(IntegrityError):
        
            comentario = Comentario.objects.create(
                conteudo="Comentario",
                perfil=self.perfil
            )

    def test_deve_gerar_excecao_quando_nao_houver_nenhum_usuario_associado(self):

        with self.assertRaises(IntegrityError):

            comentario = Comentario.objects.create(
                conteudo="Comentario",
                postagem=self.postagem
            )

    def test_deve_gerar_excecao_quando_conteudo_do_comentario_for_vazio(self):

        with self.assertRaises(ValidationError):

            comentario = Comentario.objects.create(
                perfil=self.perfil,
                postagem=self.postagem
            )

            comentario.full_clean()


    def test_deve_retornar_id_da_resposta_feita_para_o_comentario(self):

        resposta = self.comentario.responder("Comentário de resposta")

        ultima_resposta = self.comentario.respostas.latest('id')

        self.assertEquals(resposta.id,ultima_resposta.id)

    def test_deve_retornar_o_conteudo_da_resposta_corretamente(self):

        resposta = self.comentario.responder("Resposta 1")

        self.assertEquals(resposta.conteudo,"Resposta 1")

    def test_deve_retornar_respostas_associadas_ao_comentario(self):

        resposta_1 = self.comentario.responder("Resposta 1")
        resposta_2 = self.comentario.responder("Resposta 2")
        resposta_3 = self.comentario.responder("Resposta 3")

        #Obtendo somente os id das respostas no banco
        ids_resposta_banco = retornar_ids(self.comentario.respostas.all())

        #Filtrando somente os ids das respostas feitas.
        ids = retornar_ids([resposta_1, resposta_2, resposta_3])

        self.assertListEqual(ids_resposta_banco, ids)

        quantidade = self.comentario.respostas.all().count()
        self.assertEquals(quantidade,3)

    def test_todas_as_respostas_devem_ter_o_tipo_como_filho(self):

        self.comentario.responder("Resposta 1")
        self.comentario.responder("Resposta 2")
        self.comentario.responder("Resposta 3")

        tipo_verificado = lambda tipo : tipo == "FILHO"

        tipos_das_respostas = self.comentario.respostas.values_list('tipo',flat=True)
        
        condicao_geral = map(tipo_verificado,tipos_das_respostas)

        self.assertTrue(all(condicao_geral))

    def test_deve_retornar_o_id_correto_do_comentario_pai_da_resposta(self):

        comentario = Comentario.objects.create(
            conteudo="Comentário Pai",
            postagem=self.postagem,
            perfil=self.perfil
        )

        resposta = comentario.responder("Resposta 1")

        self.assertEquals(resposta.comentario_pai.id,comentario.id)

    def test_quando_responder_uma_resposta_deve_incrementar_respostas_do_comentario_pai(self):

        resposta = self.comentario.responder("Resposta 1")
        self.assertEquals(self.comentario.respostas.all().count(), 1)
    
        resposta_1 = resposta.responder("Resposta 2")
        self.assertEquals(self.comentario.respostas.all().count(), 2)

        resposta_2 = resposta_1.responder("Resposta 2")
        self.assertEquals(self.comentario.respostas.all().count(), 3)        

    def test_respostas_das_respostas_devem_constar_nas_respostas_do_comentario_geral(self):
        
        resposta = self.comentario.responder("Resposta 1")
        resposta_1 = resposta.responder("Resposta 2")
        resposta_2 = resposta_1.responder("Resposta 3")

        respostas_geral = retornar_ids(self.comentario.respostas.all())

        respostas_filhas = retornar_ids([resposta_1, resposta_2])

        self.assertTrue( set(respostas_filhas).issubset(set(respostas_geral)) )

    def test_quando_deletar_a_postagem_deletar_todos_os_comentarios_relacionados(self):

        comentario = mommy.make(Comentario,postagem=self.postagem)

        self.postagem.delete()

        comentarios_da_postagem = Comentario.objects.filter(postagem=self.postagem.id)

        self.assertEquals(0,len(comentarios_da_postagem))

    def test_quando_deletar_o_usuario_deletar_comentarios_relacionados_a_ele(self):

        comentario = mommy.make(Comentario,perfil=self.perfil,postagem=self.postagem)

        self.perfil.delete()

        comentarios_perfil = Comentario.objects.filter(perfil=self.perfil)

        self.assertEquals(0,len(comentarios_perfil))