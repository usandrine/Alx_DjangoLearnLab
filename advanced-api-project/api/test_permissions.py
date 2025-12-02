from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book

class TestTask1Requirements(APITestCase):
    """Test Task 1 requirements"""
    
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123',
            is_staff=True
        )
        
        # Create test data
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author,
            price=25.00
        )
        
        self.client = APIClient()
    
    def test_list_view_accessible(self):
        """Test ListView is accessible to anyone"""
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_view_accessible(self):
        """Test DetailView is accessible to anyone"""
        response = self.client.get(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_view_requires_auth(self):
        """Test CreateView requires authentication"""
        # Unauthenticated should fail
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Authenticated should succeed
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_view_requires_auth(self):
        """Test UpdateView requires authentication"""
        data = {'title': 'Updated Title'}
        
        # Unauthenticated should fail
        response = self.client.patch(reverse('book-update', args=[self.book.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Authenticated should succeed
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('book-update', args=[self.book.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_view_requires_auth(self):
        """Test DeleteView requires authentication"""
        # Unauthenticated should fail
        response = self.client.delete(reverse('book-delete', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Authenticated should succeed
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('book-delete', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_url_patterns_exist(self):
        """Test all required URL patterns exist"""
        urls_to_test = [
            reverse('book-list'),
            reverse('book-create'),
            reverse('book-detail', args=[1]),
            reverse('book-update', args=[1]),
            reverse('book-delete', args=[1]),
        ]
        
        for url in urls_to_test:
            response = self.client.get(url.split('?')[0])  # Remove query params
            # Should get 200, 403, or 404 (not 500 or URL error)
            self.assertIn(response.status_code, [200, 403, 404])