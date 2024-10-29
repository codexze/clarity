from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'appointment'

router = DefaultRouter()
router.register(r'', views.AppointmentModelViewSet, basename='appointments')

urlpatterns = router.urls