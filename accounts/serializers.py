from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Perfil, Disciplina, Turma, Inscricao

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', )


class PerfilSerializer(serializers.ModelSerializer):

    usuario = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset=User.objects.all())

    class Meta:
        model = Perfil
        fields = ('id', 'usuario', 'nome', 'email',)


class DisciplinaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Disciplina
		fields = ('id', 'nome')

class TurmaSerializer(serializers.ModelSerializer):
    
    professor = serializers.SlugRelatedField(slug_field=Perfil.nome, queryset=Perfil.objects.all())

    class Meta:
        model = Turma
        fields = ('id', 'professor', 'codigo', 'periodo', 'codigo_ativo',)


class InscricaoSerializer(serializers.ModelSerializer):

    perfil = serializers.SlugRelatedField(slug_field=Perfil.nome, queryset=Perfil.objects.all())
    turma = serializers.SlugRelatedField(slug_field=Turma.codigo, queryset=Turma.objects.all())

    class Meta:
        model = Inscricao
        fields = ('id', 'perfil', 'turma',)

