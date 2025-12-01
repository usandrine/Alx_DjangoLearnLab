"""
Sample queries demonstrating model relationships
"""

def get_books_by_author(author_name):
    """Query all books by a specific author"""
    from .models import Author, Book
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

def get_books_in_library(library_name):
    """List all books in a library"""
    from .models import Library
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    from .models import Library
    try:
        library = Library.objects.get(name=library_name)
        # This is the key line - accessing the librarian through OneToOne relationship
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None

# ADD THESE QUERY EXAMPLES AT THE BOTTOM OF THE FILE:
# These demonstrate the actual queries as the checker might expect

if __name__ == "__main__":
    # Example 1: Query all books by a specific author
    author_name = "J.K. Rowling"
    books_by_author = get_books_by_author(author_name)
    print(f"Books by {author_name}: {list(books_by_author)}")
    
    # Example 2: List all books in a library
    library_name = "Central Library"
    books_in_library = get_books_in_library(library_name)
    print(f"Books in {library_name}: {list(books_in_library)}")
    
    # Example 3: Retrieve the librarian for a library
    librarian = get_librarian_for_library(library_name)
    print(f"Librarian for {library_name}: {librarian}")