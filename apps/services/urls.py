from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'services'

router = DefaultRouter()
router.register(r'', views.ServiceModelViewSet, basename='services')

urlpatterns = [
    path('staff/', include('apps.services.staff.urls')),
]

urlpatterns += router.urls