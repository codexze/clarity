from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets, response, status
from rest_framework.decorators import action
from apps.core.mixins import parse_queried_date
from .serializers import *
from .models import Service

class ServiceFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = Service
        fields = ['name']

class ServicePagination(pagination.PageNumberPagination):
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

class ServiceModelViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    # filter_backends = (filters.DjangoFilterBackend)
    # filterset_class = ServiceFilter
    # pagination_class = ServicePagination
    ordering = ['name']

    def get_queryset(self):
        return  Service.objects.all()

    @action(methods=['patch'], detail=True)
    def deactivate(self, request, pk=None):
        instance = self.get_object()

        serializer = PatchServiceSerializer(instance=instance, data={'active': False}, context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        service = self.get_serializer(obj)
        return response.Response(service.data)

    @action(methods=['patch'], detail=True)
    def activate(self, request, pk=None):
        instance = self.get_object()

        serializer = PatchServiceSerializer(instance=instance, data={'active': True}, context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        service = self.get_serializer(obj)
        return response.Response(service.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateServiceSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        service = self.get_serializer(obj)
        headers = self.get_success_headers(service.data)
        return response.Response(service.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateServiceSerializer(instance=instance, data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        service = self.get_serializer(obj)
        return response.Response(service.data)
