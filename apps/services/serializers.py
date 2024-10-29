import datetime
from rest_framework import serializers
from django.utils import timezone
from apps.core.serializers import DynamicFieldsModelSerializer
from apps.authorize.serializers import UserSerializer
from .models import *


class ServiceSerializer(DynamicFieldsModelSerializer):
    display = serializers.ReadOnlyField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
    class Meta:
        model = Service
        fields = '__all__'
        # depth = 1

class CreateServiceSerializer(DynamicFieldsModelSerializer):
    created = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name field may not be empty")

        return value
    
    def validate_duration(self, value):
        if not value:
            raise serializers.ValidationError("Duration field may not be empty")

        return value
    
    def validate_price(self, value):
        if not value:
            raise serializers.ValidationError("Price field may not be empty")

        return value

    class Meta:
        model = Service
        fields = ['name', 'duration', 'price', 'created', 'created_by']


class UpdateServiceSerializer(DynamicFieldsModelSerializer):
    updated = serializers.DateTimeField(default=timezone.now)
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name field may not be empty")

        return value
    
    def validate_duration(self, value):
        if not value:
            raise serializers.ValidationError("Duration field may not be empty")

        return value
    
    def validate_price(self, value):
        if not value:
            raise serializers.ValidationError("Price field may not be empty")

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
        model = Service
        fields = ['name', 'duration', 'price', 'updated', 'updated_by', 'consistency_token']


class PatchServiceSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Service
        include = ['active']
