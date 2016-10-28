from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Perfil, Disciplina, Turma, Inscricao

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active',)


class PerfilSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset=User.objects.all())

    class Meta:
        model = Perfil
        fields = ('id', 'usuario', 'nome', 'email',)


class DisciplinaSerializer(serializers.ModelSerializer):

    qtd_inscritos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Disciplina
        fields = ('id', 'nome', 'qtd_inscritos')

    def get_qtd_inscritos(self, obj):
        qtd = Disciplina.objects.filter(pk=obj.pk).count()
        return qtd


class TurmaSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(many=False, queryset=Perfil.objects.all())
    disciplina = serializers.PrimaryKeyRelatedField(many=False, queryset=Disciplina.objects.all())

    class Meta:
        model = Turma
        fields = ('id', 'codigo', 'periodo', 'codigo_ativo', 'professor', 'disciplina')


class InscricaoSerializer(serializers.ModelSerializer):
    perfil = serializers.PrimaryKeyRelatedField(many=False, queryset=Perfil.objects.all())
    turma = serializers.PrimaryKeyRelatedField(many=False, queryset=Turma.objects.filter(codigo_ativo=True))

    class Meta:
        model = Inscricao
        fields = ('id', 'perfil', 'turma', 'criado_em')
