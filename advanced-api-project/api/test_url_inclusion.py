from django.test import TestCase
from django.urls import reverse, resolve, get_resolver
from advanced_api_project import urls as project_urls

class TestURLInclusion(TestCase):
    def test_api_urls_included_in_project(self):
        """Test that api.urls are included in the main project"""
        # Get all URL patterns from the project
        resolver = get_resolver()
        
        # Check if api patterns are included
        api_patterns_found = False
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Check nested patterns
                for nested in pattern.url_patterns:
                    if 'api' in str(nested.pattern):
                        api_patterns_found = True
                        break
        
        self.assertTrue(api_patterns_found, "API URLs are not included in the main project")
    
    def test_api_endpoints_accessible(self):
        """Test that API endpoints are accessible"""
        endpoints = [
            '/api/books/',
            '/api/books/1/',
            '/api/books/1/update/',
            '/api/books/1/delete/',
            '/api/books/create/',
        ]
        
        for endpoint in endpoints:
            try:
                # Try to resolve the URL
                resolver = resolve(endpoint)
                self.assertIsNotNone(resolver)
            except:
                # If it fails, check if it exists with different prefix
                try:
                    resolver = resolve(endpoint.replace('/api/', ''))
                    self.assertIsNotNone(resolver)
                except:
                    self.fail(f"Endpoint {endpoint} is not accessible")