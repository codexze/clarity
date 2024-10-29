from django.utils import timezone
from rest_framework import serializers
from apps.core.serializers import DynamicFieldsModelSerializer
from apps.clients.serializers import ClientSerializer
from apps.services.serializers import ServiceSerializer
from apps.services.staff.serializers import StaffSerializer

from .models import *

class AppointmentSerializer(DynamicFieldsModelSerializer):
    client = ClientSerializer()
    service = ServiceSerializer()
    employee = StaffSerializer()

    start = serializers.ReadOnlyField()
    end = serializers.ReadOnlyField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1

class CreateAppointmentSerializer(DynamicFieldsModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(source="client", queryset=Client.objects.all())
    service_id = serializers.PrimaryKeyRelatedField(source="service", queryset=Service.objects.all())
    employee_id = serializers.PrimaryKeyRelatedField(source="employee", queryset=Staff.objects.all())
    
    created = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    consistency_token = serializers.CharField(allow_null=True)

    def validate_client(self, value):
        if not value:
            raise serializers.ValidationError("Client field may not be empty")
        return value

    def validate_service(self, value):
        if not value:
            raise serializers.ValidationError("Service field may not be empty")
        return value

    def validate_employee(self, value):
        if not value:
            raise serializers.ValidationError("Employee field may not be empty")
        return value

    class Meta:
        model = Appointment
        exclude = [ 'arrived', 'arrived_time', 'cancelation', 'cancelation_reason', 'updated', "updated_by"]

class UpdateAppointmentSerializer(DynamicFieldsModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(source="client", queryset=Client.objects.all())
    service_id = serializers.PrimaryKeyRelatedField(source="service", queryset=Service.objects.all())
    employee_id = serializers.PrimaryKeyRelatedField(source="employee", queryset=Staff.objects.all())
    
    updated = serializers.DateTimeField(default=timezone.now)
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    consistency_token = serializers.CharField(allow_null=True)

    def validate_client(self, value):
        if not value:
            raise serializers.ValidationError("Client field may not be empty")
        return value

    def validate_service(self, value):
        if not value:
            raise serializers.ValidationError("Service field may not be empty")
        return value

    def validate_employee(self, value):
        if not value:
            raise serializers.ValidationError("Employee field may not be empty")
        return value
    
    def validate_consistency_token(self, value):
        if self.instance and self.instance.consistency_token:
            if self.instance.consistency_token != value:
                raise serializers.ValidationError("Consistency token match error")

        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        return instance

    class Meta:
        model = Appointment
        exclude = ['created', "created_by"]

class PatchAppointmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Client
        include = ['arrived', 'arrived_time', 'cancelation', 'cancelation_reason']