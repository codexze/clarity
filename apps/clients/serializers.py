from django.utils import timezone
from rest_framework import serializers
from apps.core.serializers import LookupListSerializer, DynamicFieldsModelSerializer
from .models import *

class ClientSerializer(DynamicFieldsModelSerializer):
    display = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    gender = LookupListSerializer(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
    class Meta:
        model = Client
        fields = '__all__'
        depth = 1

class CreateClientSerializer(DynamicFieldsModelSerializer):
    gender_id = serializers.PrimaryKeyRelatedField(source="gender", queryset=Gender.objects.all())
   
    created = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name field may not be empty")
        return value

    def validate_surname(self, value):
        if not value:
            raise serializers.ValidationError("Surname field may not be empty")
        return value

    def validate_date_of_birth(self, value):
        if not value:
            raise serializers.ValidationError("Date of Birth field may not be empty")
        return value

    def validate_mobile(self, value):
        if not value:
            raise serializers.ValidationError("Date of Birth field may not be empty")
        return value

    def validate_gender_id(self, value):
        if not value:
            return Gender.objects.get(name="Unknown")
        return value

    class Meta:
        model = Client
        fields = [ 'first_name', 'surname', 'date', 'gender', 'emailaddress', 'mobile', 'created', 'created_by']

class UpdateClientSerializer(DynamicFieldsModelSerializer):
    updated = serializers.DateTimeField(default=timezone.now)
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name field may not be empty")
        return value

    def validate_surname(self, value):
        if not value:
            raise serializers.ValidationError("Surname field may not be empty")
        return value

    def validate_date_of_birth(self, value):
        if not value:
            raise serializers.ValidationError("Date of Birth field may not be empty")
        return value

    def validate_mobile(self, value):
        if not value:
            raise serializers.ValidationError("Date of Birth field may not be empty")
        return value

    def validate_gender(self, value):
        if not value:
            return Gender.objects.get(name="Unknown")
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
        model = Client
        fields = [ 'first_name', 'surname', 'date', 'gender', 'emailaddress', 'mobile', 'updated', 'updated_by', 'consistency_token']


class PatchClientSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Client
        include = ['active']
    