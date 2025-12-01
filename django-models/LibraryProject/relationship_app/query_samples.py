from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def get_books_by_specific_author():
    """Returns all books by author named 'George Orwell'"""
    return Book.objects.filter(author__name='George Orwell')

# 2. List all books in a library
def get_all_books_in_library():
    """Returns all books in library named 'Central Library'"""
    library = Library.objects.get(name='Central Library')
    return library.books.all()

# 3. Retrieve the librarian for a library
def get_librarian_of_library():
    """Returns the librarian for library named 'Central Library'"""
    library = Library.objects.get(name='Central Library')
    return library.librarian  # This is the OneToOne relationship access