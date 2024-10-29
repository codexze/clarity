from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets, response, status
from rest_framework.decorators import action
from apps.core.mixins import parse_queried_date
from .serializers import *
from ..models import Staff, Service

class StaffFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='istartswith')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='istartswith')
    date_of_birth = filters.DateFilter(field_name='date_of_birth', lookup_expr='filter_date_of_birth')

    def filter_date_of_birth(self, queryset, name, value):
        value = parse_queried_date(value)
        if value is not None:
            queryset = queryset.filter(date_of_birth=value)
        return queryset
    
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'date_of_birth']

class StaffPagination(pagination.PageNumberPagination):
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

class StaffModelViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    # filter_backends = (filters.DjangoFilterBackend)
    # filterset_class = StaffFilter
    # pagination_class = StaffPagination
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        return  Staff.objects.all()
    
    @action(methods=['get'], detail=True)
    def services(self, request, pk=None):
        instance = self.get_object()
        queryset = Service.objects.filter(employee=instance)
        services = ServiceSerializer(queryset, many=True)
        return response.Response(services.data)
