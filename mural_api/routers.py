from rest_framework.routers import DefaultRouter

from accounts import viewsets as accounts_viewsets
from timeline import viewsets as timeline_viewsets

router = DefaultRouter()

#accounts endpoints
router.register(r'users', accounts_viewsets.UserViewSet)
router.register(r'perfil', accounts_viewsets.PerfilViewSet)

#timeline_endpoints
#router.register(r'postagens', timeline_viewsets.PostagemViewSet
