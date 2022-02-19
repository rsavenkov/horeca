import re

from django.db.models import Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters

from .models import Candidate


class CandidateFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    position = filters.CharFilter(field_name='position', lookup_expr='icontains')
    name = filters.CharFilter(method='filter_name')
    testing_status = filters.CharFilter(method='filter_testing_status')
    from_date_joined = filters.DateFilter(field_name='user__date_joined__date', lookup_expr='gte')
    to_date_joined = filters.DateFilter(field_name='user__date_joined__date', lookup_expr='lte')
    company = filters.CharFilter(field_name='creator__manager__company', lookup_expr='icontains')

    def filter_name(self, queryset, name, value):
        queryset = queryset.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))
        candidates = queryset.filter(fullname__icontains=value)
        return candidates

    def filter_testing_status(self, queryset, name, value):
        if value != 'set()':
            value = re.sub("[{}']", '', value)
            value = [arg.strip() for arg in value.split(',')]
            queryset = queryset.filter(testing_status__in=value) if value else queryset

        return queryset

    class Meta:
        model = Candidate
        fields = ['email', 'position', 'testing_status']
