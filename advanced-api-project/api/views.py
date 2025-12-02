from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from django.db import models
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter

# ============ TASK 1: REQUIRED GENERIC VIEWS ============

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    GET: Returns list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view
    
    # Filtering, searching, ordering
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'price']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    GET: Returns details of a single book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    POST: Creates a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create
    
    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    PUT/PATCH: Updates an existing book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    DELETE: Deletes a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        instance.delete()

# ============ AUTHOR VIEWS ============

class AuthorListView(generics.ListAPIView):
    """ListView for authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'birth_date']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """DetailView for single author"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class AuthorCreateView(generics.CreateAPIView):
    """CreateView for new author"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorUpdateView(generics.UpdateAPIView):
    """UpdateView for existing author"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

class AuthorDeleteView(generics.DestroyAPIView):
    """DeleteView for author"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

# ============ COMBINED VIEWS (Alternative) ============

class BookListCreateView(generics.ListCreateAPIView):
    """Combined List and Create view for books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'price']
    ordering = ['title']

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Combined Retrieve, Update, Delete view for books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

# ============ CUSTOM VIEWS ============

class BookStatisticsView(APIView):
    """Custom statistics view"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        total_books = Book.objects.count()
        total_authors = Author.objects.count()
        books_in_stock = Book.objects.filter(in_stock=True).count()
        average_price = Book.objects.aggregate(models.Avg('price'))['price__avg'] or 0
        
        return Response({
            'total_books': total_books,
            'total_authors': total_authors,
            'books_in_stock': books_in_stock,
            'average_price': float(average_price),
            'books_by_year': self.get_books_by_year()
        })
    
    def get_books_by_year(self):
        from django.db.models import Count
        return list(Book.objects.values('publication_year').annotate(count=Count('id')).order_by('-publication_year'))