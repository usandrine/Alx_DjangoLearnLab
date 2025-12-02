import requests

BASE_URL = 'http://127.0.0.1:8000/api/books/'

def test_all_requirements():
    print("Testing all Task 2 requirements...")
    
    # 1. Test filtering by title
    print("\n1. Testing filter by title:")
    response = requests.get(BASE_URL + '?title=Harry')
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json().get('results', []))}")
    
    # 2. Test filtering by author
    print("\n2. Testing filter by author:")
    response = requests.get(BASE_URL + '?author__name=Rowling')
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json().get('results', []))}")
    
    # 3. Test filtering by publication_year
    print("\n3. Testing filter by publication_year:")
    response = requests.get(BASE_URL + '?publication_year=1997')
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json().get('results', []))}")
    
    # 4. Test search functionality (title and author)
    print("\n4. Testing search functionality:")
    response = requests.get(BASE_URL + '?search=Harry')
    print(f"   Search 'Harry': {response.status_code}")
    
    response = requests.get(BASE_URL + '?search=Rowling')
    print(f"   Search 'Rowling': {response.status_code}")
    
    # 5. Test ordering
    print("\n5. Testing ordering:")
    response = requests.get(BASE_URL + '?ordering=title')
    print(f"   Order by title: {response.status_code}")
    
    response = requests.get(BASE_URL + '?ordering=-publication_year')
    print(f"   Order by -publication_year: {response.status_code}")
    
    # 6. Test combined filters
    print("\n6. Testing combined filters:")
    response = requests.get(BASE_URL + '?title__icontains=Harry&publication_year__gt=1995')
    print(f"   Title contains Harry AND year > 1995: {response.status_code}")

if __name__ == "__main__":
    test_all_requirements()