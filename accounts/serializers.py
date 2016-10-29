from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Perfil, Disciplina, Turma, Inscricao

from django.urls import reverse

from django.utils.translation import ugettext_lazy as _


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


class PerfilSignUpSerializer(serializers.Serializer):
    usuario =  serializers.SlugField(required=True, allow_blank=False, max_length=50)
    nome = serializers.CharField(required=True)
    email = serializers.EmailField()
    senha = serializers.CharField(min_length=6, required=True, write_only=True)

    def create(self, validated_data):
        usuario = validated_data.get('usuario')
        email = validated_data.get('email')
        senha = validated_data.get('senha')
        nome = validated_data.get('nome')

        user = User.objects.create_user(username=usuario, email=email, password=senha)
        perfil = Perfil(usuario=user, nome=nome, email=email)
        perfil.save()

        return perfil

    def validate_usuario(self, value):
        if User.objects.filter(username=value).exists():
            msg = _('Usuário já existe.')
            raise serializers.ValidationError(msg)

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists() or Perfil.objects.filter(email=value):
            msg = _('Email já cadastrado.')
            raise serializers.ValidationError(msg)

        return value


class DisciplinaSerializer(serializers.ModelSerializer):

    turmas = serializers.StringRelatedField(many=True)

    class Meta:
        model = Disciplina
        fields = ('id', 'nome', 'turmas')


class TurmaSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(many=False, queryset=Perfil.objects.all())
    disciplina = serializers.PrimaryKeyRelatedField(many=False, queryset=Disciplina.objects.all())
    qtd_inscritos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Turma
        fields = ('id', 'codigo', 'periodo', 'codigo_ativo', 'professor', 'disciplina', 'qtd_inscritos')

    def get_qtd_inscritos(self, obj):
        qtd = Inscricao.objects.filter(turma=obj).count()
        return qtd


class InscricaoSerializer(serializers.ModelSerializer):
    perfil = serializers.PrimaryKeyRelatedField(many=False, queryset=Perfil.objects.all())
    turma = serializers.PrimaryKeyRelatedField(many=False, queryset=Turma.objects.filter(codigo_ativo=True))

    class Meta:
        model = Inscricao
        fields = ('id', 'perfil', 'turma', 'criado_em')
