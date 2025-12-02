from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter

# ============ BOOK VIEWS ============

class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    GET: Returns list of all books
    POST: Creates a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', 'isbn']
    ordering_fields = ['title', 'publication_year', 'price']
    ordering = ['title']

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        """Custom update logic if needed"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Custom delete logic if needed"""
        instance.delete()

# ============ AUTHOR VIEWS ============

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    List all authors or create a new author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'birth_date']
    ordering = ['name']

class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an author instance.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_destroy(self, instance):
        """Prevent deletion if author has books"""
        if instance.books.exists():
            return Response(
                {'error': 'Cannot delete author with existing books. Delete books first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()

# ============ CUSTOM VIEWS ============

class BookStatisticsView(APIView):
    """
    Custom view to provide book statistics.
    """
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
        """Helper method to get book count by publication year"""
        from django.db.models import Count
        return list(Book.objects.values('publication_year').annotate(count=Count('id')).order_by('-publication_year'))

class AuthorBooksView(APIView):
    """
    Custom view to get books by a specific author.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, author_id):
        author = get_object_or_404(Author, id=author_id)
        books = Book.objects.filter(author=author)
        serializer = BookSerializer(books, many=True)
        
        return Response({
            'author': author.name,
            'total_books': books.count(),
            'books': serializer.data
        })