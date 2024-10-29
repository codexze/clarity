from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'clients'

router = DefaultRouter()
router.register(r'', views.ClientModelViewSet, basename='clients')

urlpatterns = router.urls