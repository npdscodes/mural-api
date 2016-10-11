from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from .models import Perfil

User = get_user_model()


class UserSerializer(ModelSerializer):

    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', )


class PerfilSerializer(ModelSerializer):

    usuario = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD)

    class Meta:
        model = Perfil
        fields = ('id', 'usuario', 'nome', 'email',)

