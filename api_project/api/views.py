from rest_framework import generics, viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# Task 1: Simple List View with permissions
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    GET: Returns list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view

# Task 2: ViewSet for CRUD operations with permissions
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model that provides CRUD operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read for anyone, write for authenticated

# Task 3: Custom Token View to return user details with token
class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom token view that returns user details along with token
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })