# test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve
from api import views

class TestURLPatterns(TestCase):
    def test_book_update_url_pattern(self):
        """Test that books/update URL pattern exists"""
        # Try to resolve the URL pattern
        url = reverse('book-update', args=[1])
        self.assertEqual(url, '/api/books/1/update/')
        
        # Or check if pattern exists
        resolver = resolve('/api/books/1/update/')
        self.assertEqual(resolver.func.__name__, 'BookUpdateView')
    
    def test_book_delete_url_pattern(self):
        """Test that books/delete URL pattern exists"""
        url = reverse('book-delete', args=[1])
        self.assertEqual(url, '/api/books/1/delete/')
        
        resolver = resolve('/api/books/1/delete/')
        self.assertEqual(resolver.func.__name__, 'BookDeleteView')
    
    def test_all_url_patterns_exist(self):
        """Test all required URL patterns"""
        patterns = [
            ('book-list', None, '/api/books/'),
            ('book-create', None, '/api/books/create/'),
            ('book-detail', 1, '/api/books/1/'),
            ('book-update', 1, '/api/books/1/update/'),
            ('book-delete', 1, '/api/books/1/delete/'),
        ]
        
        for name, pk, expected in patterns:
            if pk:
                url = reverse(name, args=[pk])
            else:
                url = reverse(name)
            self.assertEqual(url, expected)