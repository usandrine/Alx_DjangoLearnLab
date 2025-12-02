import requests

BASE_URL = 'http://127.0.0.1:8000/api'

def test_filtering():
    """Test filtering capabilities"""
    print("Testing Filtering...")
    
    # Filter by year
    response = requests.get(f"{BASE_URL}/books/?publication_year=1997")
    print(f"Filter by year 1997: {response.status_code}")
    
    # Filter by price range
    response = requests.get(f"{BASE_URL}/books/?min_price=20&max_price=40")
    print(f"Filter by price range 20-40: {response.status_code}")
    
    # Filter by author name
    response = requests.get(f"{BASE_URL}/books/?author__name__icontains=Rowling")
    print(f"Filter by author name 'Rowling': {response.status_code}")
    
    # Filter by in_stock
    response = requests.get(f"{BASE_URL}/books/?in_stock=true")
    print(f"Filter by in_stock=true: {response.status_code}")

def test_searching():
    """Test searching capabilities"""
    print("\nTesting Searching...")
    
    # Search by title
    response = requests.get(f"{BASE_URL}/books/?search=Harry")
    print(f"Search for 'Harry': {response.status_code}")
    
    # Search by author name
    response = requests.get(f"{BASE_URL}/books/?search=Rowling")
    print(f"Search for 'Rowling': {response.status_code}")
    
    # Search in authors
    response = requests.get(f"{BASE_URL}/authors/?search=British")
    print(f"Search authors for 'British': {response.status_code}")

def test_ordering():
    """Test ordering capabilities"""
    print("\nTesting Ordering...")
    
    # Order by title ascending
    response = requests.get(f"{BASE_URL}/books/?ordering=title")
    print(f"Order by title ascending: {response.status_code}")
    
    # Order by price descending
    response = requests.get(f"{BASE_URL}/books/?ordering=-price")
    print(f"Order by price descending: {response.status_code}")
    
    # Order by publication year descending
    response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
    print(f"Order by publication year descending: {response.status_code}")
    
    # Order authors by name
    response = requests.get(f"{BASE_URL}/authors/?ordering=name")
    print(f"Order authors by name: {response.status_code}")

if __name__ == "__main__":
    test_filtering()
    test_searching()
    test_ordering()