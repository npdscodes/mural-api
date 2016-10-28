from rest_framework.routers import DefaultRouter

from accounts import viewsets as accounts_viewsets
from timeline import viewsets as timeline_viewsets

router = DefaultRouter()

#accounts endpoints
router.register(r'users', accounts_viewsets.UserViewSet)
router.register(r'perfis', accounts_viewsets.PerfilViewSet)
router.register(r'disciplinas', accounts_viewsets.DisciplinaViewSet)
router.register(r'turmas', accounts_viewsets.TurmaViewSet)
router.register(r'inscricoes', accounts_viewsets.InscricaoViewSet)

#timeline_endpoints
#router.register(r'postagens', timeline_viewsets.PostagemViewSet
