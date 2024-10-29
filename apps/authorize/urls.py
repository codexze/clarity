from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'roles', views.GroupModelViewSet, basename='frontend-roles')

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('current/', views.UserView.as_view()),
    # path('session/user/active/', views.SessionUserActiveView.as_view()),
    
    path('permissions/', views.PermissionsView.as_view()),
]

urlpatterns += router.urls