from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model with custom validation"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name', 'isbn', 'price', 'in_stock']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """Validate that publication year is not in the future"""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid year (1000 or later)."
            )
        return value
    
    def validate(self, data):
        """Validate the entire book data"""
        # Additional cross-field validation can be added here
        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError({
                'price': 'Price cannot be negative.'
            })
        return data

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model with nested books"""
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date', 'books', 'book_count']
        read_only_fields = ['id', 'book_count']
    
    def validate_name(self, value):
        """Validate author name"""
        if len(value) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        return value