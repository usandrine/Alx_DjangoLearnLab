"""
Unit tests for API views as required by Task 3
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book

class TestBookAPIViews(APITestCase):
    """Test cases specifically for Book API views"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.author = Author.objects.create(name='J.K. Rowling')
        self.book = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author,
            price=29.99
        )
    
    def test_book_list_view_status_code(self):
        """Test that book list view returns 200 OK"""
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_detail_view_status_code(self):
        """Test that book detail view returns 200 OK"""
        response = self.client.get(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_requires_authentication(self):
        """Test that creating a book requires authentication"""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_can_create_book(self):
        """Test authenticated user can create a book"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Authenticated Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        url = f"{reverse('book-list-create')}?title__icontains=Harry"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_books(self):
        """Test searching books"""
        url = f"{reverse('book-list-create')}?search=Potter"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_order_books_by_title(self):
        """Test ordering books by title"""
        Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author,
            price=19.99
        )
        
        url = f"{reverse('book-list-create')}?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['Animal Farm', 'Harry Potter'])