import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """Filter for Book model with custom filters"""
    # Custom filters
    min_year = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        label='Minimum publication year'
    )
    max_year = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        label='Maximum publication year'
    )
    min_price = django_filters.NumberFilter(
        field_name='price', 
        lookup_expr='gte',
        label='Minimum price'
    )
    max_price = django_filters.NumberFilter(
        field_name='price', 
        lookup_expr='lte',
        label='Maximum price'
    )
    
    # Filter by author name (case-insensitive contains)
    author_name = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains',
        label='Author name contains'
    )
    
    # Filter by exact title
    title_exact = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='exact',
        label='Exact title match'
    )
    
    # Filter by title contains (case-insensitive)
    title_contains = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        label='Title contains'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'startswith'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author__name': ['exact', 'icontains'],
            'isbn': ['exact'],
            'price': ['exact', 'gte', 'lte'],
            'in_stock': ['exact'],
        }