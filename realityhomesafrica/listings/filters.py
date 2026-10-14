import django_filters
from .models import Property, PROPERTY_TYPES, NIGERIAN_STATES


class PropertyFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains', label='City')
    state = django_filters.ChoiceFilter(choices=NIGERIAN_STATES, label='State', empty_label='All States')
    property_type = django_filters.ChoiceFilter(choices=PROPERTY_TYPES, label='Type', empty_label='All Types')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price (₦)')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price (₦)')
    min_bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte', label='Min Bedrooms')

    class Meta:
        model = Property
        fields = ['city', 'state', 'property_type', 'min_price', 'max_price', 'min_bedrooms']
