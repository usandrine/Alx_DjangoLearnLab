import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """Filter for Book model with custom filters"""
    min_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = {
            'title': ['icontains', 'exact'],
            'publication_year': ['exact'],
            'in_stock': ['exact'],
            'author__name': ['icontains'],
        }