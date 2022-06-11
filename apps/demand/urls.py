from rest_framework.routers import SimpleRouter

from .views import DemandViewset, ProjectViewset, RecordViewset


router = SimpleRouter()
router.register('demand', DemandViewset)
router.register('project', ProjectViewset)
router.register('record', RecordViewset)

urlpatterns = []

urlpatterns += router.urls