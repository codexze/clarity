import datetime
from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets, response, status
from rest_framework.decorators import action
from apps.core.mixins import parse_queried_date
from .serializers import *
from .models import Appointment

class AppointmentModelViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.select_related('client', 'service', 'employee')
    
    @action(methods=['patch'], detail=True)
    def arrived(self, request, pk=None):
        instance = self.get_object()

        serializer = PatchAppointmentSerializer(instance=instance, data=request.data, context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        arrived_time = datetime.datetime.now().time() if request.data.get('arrived') else None
        obj = serializer.save(arrived_time=arrived_time)
        appointment = self.get_serializer(obj)
        return response.Response(appointment.data)

    @action(methods=['patch'], detail=True)
    def cancelled(self, request, pk=None):
        instance = self.get_object()

        serializer = PatchAppointmentSerializer(instance=instance, data=request.data, context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        appointment = self.get_serializer(obj)
        return response.Response(appointment.data)
    
    def create(self, request):
        serializer = CreateAppointmentSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        appointment = self.get_serializer(obj)
        return response.Response(appointment.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateAppointmentSerializer(instance=instance, data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        appointment = self.get_serializer(obj)
        return response.Response(appointment.data)
    
