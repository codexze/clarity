from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from .models import User, FrontendPermission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(source="permissions", queryset=Permission.objects.all(), many=True, allow_null=True, required=False)

    class Meta:
        model = Group
        fields = '__all__'

class FrontendPermissionSerializer(serializers.ModelSerializer):
    view_permissions = PermissionSerializer(many=True, read_only=True)
    add_permissions = PermissionSerializer(many=True, read_only=True)
    change_permissions = PermissionSerializer(many=True, read_only=True)
    delete_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = FrontendPermission
        exclude = ['id']

class UserSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    roles = GroupSerializer(source="groups", many=True, read_only=True)

    class Meta:
        model = User
        # exclude = ['password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined']
        exclude = ['password', 'user_permissions', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

class UserLimitedSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(error_messages={'null': 'Your username is required', 'blank': 'Your username is required'})
    password = serializers.CharField(error_messages={'null': 'Your password is required', 'blank': 'Your password is required'})

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}