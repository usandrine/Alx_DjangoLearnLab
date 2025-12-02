import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """Filter for Book model that allows filtering by title, author, and publication_year"""
    
    # Custom filters for better control
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']