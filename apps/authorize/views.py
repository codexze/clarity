from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import Http404
from rest_framework import views, generics, viewsets, response, permissions, authentication
from rest_framework.decorators import action
from .models import User, FrontendPermission
from .serializers import *

# Create your views here.
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        
        return response.Response(UserSerializer(user).data)

class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        logout(request)
        return response.Response()
    

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def put(self, request, format=None):
        obj = self.request.user
        serializer = UserSerializer(obj, data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = UserSerializer(user)
        return response.Response(serializer.data)

class PermissionsView(views.APIView):
    def get_object(self):
        try:
            return FrontendPermission.objects.prefetch_related('view_permissions', 'add_permissions', 'change_permissions', 'delete_permissions').first()
        except FrontendPermission.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        obj = self.get_object()
        serializer = FrontendPermissionSerializer(obj)
        return response.Response(serializer.data)

class GroupModelViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.prefetch_related('permissions').all().order_by('name')

