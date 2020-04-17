from rest_framework.routers import DefaultRouter
from accounts.api.views import DoctorViewSet, PatientViewSet, UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r"patient", PatientViewSet)
router.register(r"doctor", DoctorViewSet)


urlpatterns = []

urlpatterns += router.urls
