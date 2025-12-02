from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from django.db import models
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter

# ============ BOOK VIEWS WITH PROPER PERMISSION CLASSES ============

class BookListView(generics.ListAPIView):
    """
    ListView: Retrieve all books
    Permission: AllowAny (unauthenticated users can view)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Explicitly allow anyone
    
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
    DetailView: Retrieve single book by ID
    Permission: AllowAny (unauthenticated users can view)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Explicitly allow anyone
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Add new book
    Permission: IsAuthenticated (only logged-in users can create)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated
    
    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modify existing book
    Permission: IsAuthenticated (only logged-in users can update)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Remove book
    Permission: IsAuthenticated (only logged-in users can delete)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        instance.delete()

# ============ AUTHOR VIEWS WITH PROPER PERMISSION CLASSES ============

class AuthorListView(generics.ListAPIView):
    """
    ListView: Retrieve all authors
    Permission: AllowAny
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'birth_date']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieve single author by ID
    Permission: AllowAny
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class AuthorCreateView(generics.CreateAPIView):
    """
    CreateView: Add new author
    Permission: IsAuthenticated
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modify existing author
    Permission: IsAuthenticated
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

class AuthorDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Remove author
    Permission: IsAuthenticated
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

# ============ COMBINED VIEWS ============

class BookListCreateView(generics.ListCreateAPIView):
    """Combined view with IsAuthenticatedOrReadOnly permission"""
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
    """Combined view with IsAuthenticatedOrReadOnly permission"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

# ============ ROLE-BASED PERMISSION EXAMPLE ============

class AdminOnlyView(APIView):
    """
    Example of role-based permission
    Only users with is_staff=True can access
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        return Response({
            'message': 'This view is only accessible to admin users',
            'user': request.user.username
        })

class LibrarianOnlyView(APIView):
    """
    Example of custom permission based on user role
    (You would need to implement custom permission class)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user has librarian role (pseudo-code)
        # if request.user.profile.role == 'librarian':
        return Response({
            'message': 'Librarian dashboard',
            'user': request.user.username
        })

# ============ CUSTOM VIEWS ============

class BookStatisticsView(APIView):
    """Public statistics view"""
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