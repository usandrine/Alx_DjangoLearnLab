import os
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        'api/models.py',
        'api/serializers.py', 
        'api/views.py',
        'api/urls.py',
        'api_project/urls.py',
        'api_project/settings.py',
    ]
    
    print("Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (MISSING)")
    
    return all(os.path.exists(f) for f in required_files)

def check_imports():
    """Check if views.py has required imports"""
    with open('api/views.py', 'r') as f:
        content = f.read()
        
        required = [
            'from rest_framework import generics',
            'from rest_framework import viewsets',
            'permissions.IsAuthenticatedOrReadOnly',
            'ObtainAuthToken',
        ]
        
        print("\nChecking imports in api/views.py...")
        for req in required:
            if req in content:
                print(f"✓ {req}")
            else:
                print(f"✗ {req} (MISSING)")
    
    return True

def main():
    print("Verifying API Project Setup...")
    print("=" * 50)
    
    if check_files() and check_imports():
        print("\n✓ Project setup appears correct!")
        print("\nTo test:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/api/books/")
        print("3. Test authentication: http://127.0.0.1:8000/api/api-token-auth/")
    else:
        print("\n✗ Project has issues that need fixing")

if __name__ == "__main__":
    main()