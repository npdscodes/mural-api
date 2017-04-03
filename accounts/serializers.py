from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Perfil, Disciplina, Turma, Inscricao

from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active',)


class PerfilSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, read_only=True)
    login = serializers.SlugField(required=True, write_only=True)
    senha = serializers.CharField(required=True, min_length=4, allow_blank=False, write_only=True)

    class Meta:
        model = Perfil
        fields = ('id', 'usuario', 'login', 'nome', 'email','senha')


    def validate_login(self, value):
        if User.objects.filter(username=value).exists():
            msg = _('Já existe um Perfil para este login: {}'.format(value))
            raise serializers.ValidationError(msg)

        return value


class DisciplinaSerializer(serializers.ModelSerializer):

    turmas = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Disciplina
        fields = ('id', 'nome', 'turmas')


class TurmaSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(many=False, queryset=Perfil.objects.all())
    disciplina = serializers.PrimaryKeyRelatedField(many=False, queryset=Disciplina.objects.all())
    qtd_inscritos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Turma
        fields = ('id', 'codigo', 'nome', 'periodo', 'codigo_ativo', 'professor', 'disciplina', 'qtd_inscritos')
        fields = ('id', 'criado_em','codigo', 'periodo', 'codigo_ativo', 'professor', 'disciplina', 'qtd_inscritos')

    def get_qtd_inscritos(self, obj):
        qtd = Inscricao.objects.filter(turma=obj).count()
        return qtd


class InscricaoSerializer(serializers.ModelSerializer):
    perfil = serializers.PrimaryKeyRelatedField(many=False, queryset=Perfil.objects.all())
    turma = serializers.PrimaryKeyRelatedField(many=False, queryset=Turma.objects.filter(codigo_ativo=True))

    class Meta:
        model = Inscricao
        fields = ('id', 'perfil', 'turma', 'criado_em')
