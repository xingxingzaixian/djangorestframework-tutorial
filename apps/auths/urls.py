from rest_framework.routers import SimpleRouter

from auths.views import RoleViewset

router = SimpleRouter()
router.register('role', RoleViewset)

urlpatterns = []

urlpatterns += router.urls