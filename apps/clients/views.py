from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets, response, status
from rest_framework.decorators import action
from apps.core.mixins import parse_queried_date
from apps.appointments.serializers import AppointmentSerializer
from apps.appointments.models import Appointment
from .serializers import *
from .models import Client

class ClientFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='istartswith')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='istartswith')
    date_of_birth = filters.DateFilter(field_name='date_of_birth', lookup_expr='filter_date_of_birth')
    emailaddress = filters.CharFilter(field_name='emailaddress', lookup_expr='istartswith')
    mobile = filters.CharFilter(field_name='mobile', lookup_expr='istartswith')
    active = filters.BooleanFilter() 

    def filter_date_of_birth(self, queryset, name, value):
        value = parse_queried_date(value)
        if value is not None:
            queryset = queryset.filter(date_of_birth=value)
        return queryset
    
    class Meta:
        model = Client
        fields = [ 'first_name', 'last_name', 'date_of_birth', 'emailaddress', 'mobile', 'active']


class ClientPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    page_query_param = "page"
    max_page_size = 10
    # display_page_controls = False
    # template = None

    def start_index(self):
        """
        Return the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.page.paginator.count == 0:
            return 0
        return (self.page.paginator.per_page * (self.page.number - 1)) + 1

    def end_index(self):
        """
        Return the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.page.number == self.page.paginator.num_pages:
            return self.page.paginator.count
        return self.page.number * self.page.paginator.per_page

    def get_paginated_response(self, data):
        return response.Response({
            'start_index': self.start_index(),
            'end_index': self.end_index(),
            'tot_rows': self.page.paginator.count,
            'items': data
        })
    
class ClientModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    # filter_backends = (filters.DjangoFilterBackend)
    # filterset_class = ClientFilter
    # pagination_class = ClientPagination
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        return  Client.objects.all()
    
    @action(methods=['patch'], detail=True)
    def deactivate(self, request, pk=None):
        instance = self.get_object()

        serializer = PatchClientSerializer(instance=instance, data={'active': False}, context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        client = self.get_serializer(obj)
        return response.Response(client.data)

    @action(methods=['patch'], detail=True)
    def activate(self, request, pk=None):
        instance = self.get_object()

        serializer = PatchClientSerializer(instance=instance, data={'active': True}, context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        client = self.get_serializer(obj)
        return response.Response(client.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateClientSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        client = self.get_serializer(obj)
        headers = self.get_success_headers(client.data)
        return response.Response(client.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateClientSerializer(instance=instance, data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        client = self.get_serializer(obj)
        return response.Response(client.data)
    
    @action(methods=['get'], detail=True)
    def appointments(self, request, pk=None):
        instance = self.get_object()
        queryset = Appointment.objects.filter(client=instance)
        clients = AppointmentSerializer(queryset, many=True)
        return response.Response(clients.data)

