from django.contrib.auth import get_user_model

from rest_framework import viewsets

from .serializers import UserSerializer, PerfilSerializer, DisciplinaSerializer, TurmaSerializer, InscricaoSerializer

from .models import Perfil, Disciplina, Turma, Inscricao

from .mixins import ViewsetPadraoMixin


User = get_user_model()


class UserViewSet(ViewsetPadraoMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD,)
    pagination_class = None
    ordering_fields = ('username', 'first_name', 'last_name', 'email')


class PerfilViewSet(ViewsetPadraoMixin, viewsets.ModelViewSet):
    """Endpoint para a criação e listagem de perfis"""

    queryset = Perfil.objects.order_by('nome')
    serializer_class = PerfilSerializer
    search_fields = ('nome', 'email',)
    ordering_fields = ('nome', 'email',)


class DisciplinaViewSet(ViewsetPadraoMixin, viewsets.ModelViewSet):
    """Endpoint para a criação e listagem das disciplinas"""

    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    search_fields = ('nome',)
    ordering_fields = ('nome',)


class TurmaViewSet(ViewsetPadraoMixin, viewsets.ModelViewSet):
    """Endpoint para a criação e listagem das turmas"""

    queryset = Turma.objects.order_by('codigo')
    serializer_class = TurmaSerializer
    search_fields = ('professor', 'codigo',)
    ordering_fields = ('codigo',)


class InscricaoViewSet(ViewsetPadraoMixin, viewsets.ModelViewSet):
    """Endpoint para a criação e listagem das inscrições"""

    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    search_fields = ('perfil', 'turma',)
    ordering_fields = ('perfil', 'turma',)