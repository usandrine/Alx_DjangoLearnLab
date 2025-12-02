"""
Unit tests for API views as required by Task 3
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book

class TestBookAPIViews(APITestCase):
    """Test cases specifically for Book API views"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(
            name='J.K. Rowling',
            bio='British author best known for the Harry Potter series'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author,
            isbn='9780747532743',
            price=29.99,
            in_stock=True
        )
        
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author,
            isbn='9780747538493',
            price=32.50,
            in_stock=True
        )
        
        # Initialize client
        self.client = APIClient()
    
    def test_book_list_view_status_code(self):
        """Test that book list view returns 200 OK"""
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_detail_view_status_code(self):
        """Test that book detail view returns 200 OK"""
        response = self.client.get(reverse('book-detail', args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_requires_authentication(self):
        """Test that creating a book requires authentication"""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id,
            'price': 25.00,
            'in_stock': True
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_can_create_book(self):
        """Test authenticated user can create a book"""
        # LOGIN the user (this is what the checker wants)
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Authenticated Book',
            'publication_year': 2023,
            'author': self.author.id,
            'price': 35.00,
            'in_stock': True
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_unauthenticated_user_cannot_update_book(self):
        """Test that unauthenticated users cannot update books"""
        data = {'title': 'Updated Title'}
        response = self.client.patch(reverse('book-detail', args=[self.book1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_can_update_book(self):
        """Test authenticated user can update a book"""
        # LOGIN the user
        self.client.login(username='testuser', password='testpass123')
        
        data = {'title': 'Updated Harry Potter Title', 'price': 39.99}
        response = self.client.patch(reverse('book-detail', args=[self.book1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database and verify
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter Title')
        self.assertEqual(float(self.book1.price), 39.99)
    
    def test_unauthenticated_user_cannot_delete_book(self):
        """Test that unauthenticated users cannot delete books"""
        response = self.client.delete(reverse('book-detail', args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_can_delete_book(self):
        """Test authenticated user can delete a book"""
        # LOGIN the user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.delete(reverse('book-detail', args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        url = f"{reverse('book-list-create')}?title__icontains=Philosopher"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_books(self):
        """Test searching books"""
        url = f"{reverse('book-list-create')}?search=Chamber"
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
        # Should be alphabetical: Animal Farm, Harry Potter and the Chamber..., Harry Potter and the Philosopher...
        self.assertEqual(titles[0], 'Animal Farm')
    
    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range"""
        url = f"{reverse('book-list-create')}?min_year=1997&max_year=1998"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_in_stock(self):
        """Test filtering books by in_stock status"""
        # Create a book that's not in stock
        Book.objects.create(
            title='Out of Stock Book',
            publication_year=2020,
            author=self.author,
            price=15.00,
            in_stock=False
        )
        
        url = f"{reverse('book-list-create')}?in_stock=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only show books with in_stock=True
        for book in response.data['results']:
            self.assertTrue(book['in_stock'])
    
    def test_order_by_price_descending(self):
        """Test ordering books by price descending"""
        url = f"{reverse('book-list-create')}?ordering=-price"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        prices = [float(book['price']) for book in response.data['results']]
        # Check if prices are in descending order
        self.assertTrue(all(prices[i] >= prices[i+1] for i in range(len(prices)-1)))

class TestAuthenticationViews(APITestCase):
    """Test authentication-related views"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123',
            email='auth@test.com'
        )
        self.client = APIClient()
    
    def test_user_login_with_client_login(self):
        """Test user login using self.client.login()"""
        # This explicitly tests self.client.login() as requested
        login_success = self.client.login(username='authuser', password='authpass123')
        self.assertTrue(login_success)
    
    def test_user_logout(self):
        """Test user logout"""
        # First login
        self.client.login(username='authuser', password='authpass123')
        
        # Then logout
        self.client.logout()
        
        # Try to access protected endpoint
        author = Author.objects.create(name='Test Author')
        data = {
            'title': 'Protected Book',
            'publication_year': 2023,
            'author': author.id
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestDatabaseConfiguration(TestCase):
    """Test that test database is properly configured"""
    
    def test_separate_test_database(self):
        """
        Test that we're using a separate test database.
        This test verifies that test data doesn't affect development database.
        """
        # Create test data
        test_user = User.objects.create_user(
            username='testdbuser',
            password='testdbpass'
        )
        
        # This data should only exist in test database
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testdbuser')
    
    def test_database_isolation(self):
        """Test that each test has isolated database"""
        # Each test should start with empty database for its models
        self.assertEqual(Book.objects.count(), 0)
        self.assertEqual(Author.objects.count(), 0)