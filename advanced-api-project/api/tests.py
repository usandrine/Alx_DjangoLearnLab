from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """Test cases for Book API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(
            name='Test Author',
            bio='Test bio'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            publication_year=2020,
            author=self.author,
            isbn='1234567890123',
            price=29.99,
            in_stock=True
        )
        
        self.book2 = Book.objects.create(
            title='Test Book 2',
            publication_year=2019,
            author=self.author,
            isbn='9876543210987',
            price=19.99,
            in_stock=False
        )
        
        # Set up client
        self.client = APIClient()
    
    # ============ AUTHENTICATION TESTS ============
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users can read but not write"""
        # GET should work
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # POST should fail for unauthenticated users
        response = self.client.post(reverse('book-list-create'), {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_access(self):
        """Test that authenticated users can create books"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(reverse('book-list-create'), {
            'title': 'Authenticated Book',
            'publication_year': 2023,
            'author': self.author.id,
            'price': 39.99,
            'in_stock': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
    
    # ============ CRUD OPERATION TESTS ============
    
    def test_list_books(self):
        """Test listing all books"""
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_book(self):
        """Test retrieving a single book"""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
    
    def test_create_book(self):
        """Test creating a new book"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2022,
            'author': self.author.id,
            'price': 25.50,
            'in_stock': True
        }
        
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Test Book')
    
    def test_update_book(self):
        """Test updating a book"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-detail', args=[self.book1.id])
        data = {'title': 'Updated Title', 'price': 35.00}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        self.assertEqual(float(self.book1.price), 35.00)
    
    def test_delete_book(self):
        """Test deleting a book"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    # ============ VALIDATION TESTS ============
    
    def test_publication_year_validation(self):
        """Test that future publication years are rejected"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Future Book',
            'publication_year': 2050,  # Future year
            'author': self.author.id
        }
        
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_price_validation(self):
        """Test that negative prices are rejected"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Negative Price Book',
            'publication_year': 2020,
            'author': self.author.id,
            'price': -10.00
        }
        
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ============ FILTERING TESTS ============
    
    def test_filter_by_year(self):
        """Test filtering books by publication year"""
        url = reverse('book-list-create') + '?publication_year=2020'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_filter_by_in_stock(self):
        """Test filtering books by stock status"""
        url = reverse('book-list-create') + '?in_stock=true'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_min_max_year_filter(self):
        """Test filtering with min_year and max_year"""
        url = reverse('book-list-create') + '?min_year=2019&max_year=2020'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    # ============ SEARCHING TESTS ============
    
    def test_search_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list-create') + '?search=Book 1'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_search_by_author_name(self):
        """Test searching books by author name"""
        url = reverse('book-list-create') + '?search=Author'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    # ============ ORDERING TESTS ============
    
    def test_ordering_by_title(self):
        """Test ordering books by title"""
        url = reverse('book-list-create') + '?ordering=title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in response.data['results']]
        self.assertEqual(titles, ['Test Book 1', 'Test Book 2'])
    
    def test_ordering_by_price_desc(self):
        """Test ordering books by price descending"""
        url = reverse('book-list-create') + '?ordering=-price'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(item['price']) for item in response.data['results']]
        self.assertEqual(prices, [29.99, 19.99])
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year"""
        url = reverse('book-list-create') + '?ordering=-publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item['publication_year'] for item in response.data['results']]
        self.assertEqual(years, [2020, 2019])
    
    # ============ CUSTOM ENDPOINT TESTS ============
    
    def test_statistics_endpoint(self):
        """Test the statistics endpoint"""
        url = reverse('book-statistics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_books', response.data)
        self.assertEqual(response.data['total_books'], 2)
        self.assertEqual(response.data['total_authors'], 1)
    
    def test_author_books_endpoint(self):
        """Test getting books by author"""
        url = reverse('author-books', args=[self.author.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'], 'Test Author')
        self.assertEqual(response.data['total_books'], 2)
        self.assertEqual(len(response.data['books']), 2)

class AuthorAPITestCase(APITestCase):
    """Test cases for Author API endpoints"""
    
    def setUp(self):
        self.author = Author.objects.create(
            name='Test Author',
            bio='Test Biography'
        )
        self.client = APIClient()
    
    def test_list_authors(self):
        response = self.client.get(reverse('author-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_author(self):
        data = {'name': 'New Author', 'bio': 'New Bio'}
        response = self.client.post(reverse('author-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_author_validation(self):
        data = {'name': 'A'}  # Too short
        response = self.client.post(reverse('author-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)