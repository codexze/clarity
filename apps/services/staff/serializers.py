import datetime
from rest_framework import serializers
from django.utils import timezone
from apps.core.serializers import DynamicFieldsModelSerializer
from apps.authorize.serializers import UserSerializer
from ..serializers import ServiceSerializer
from ..models import *

class StaffSerializer(UserSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    class Meta:
        model = User
        exclude = []


class StaffServicesSerializer(DynamicFieldsModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(source="employee", queryset=User.objects.all(), allow_null=False)
    service_id = serializers.PrimaryKeyRelatedField(source="service", queryset=Service.objects.all(), allow_null=False)
    
    employee = UserSerializer()
    service = ServiceSerializer()

    class Meta:
        model = StaffServices
        include = ['__all__']
        depth = 1