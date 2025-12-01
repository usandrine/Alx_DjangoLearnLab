```python
# Delete the book
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Confirm deletion
books = Book.objects.all()
print(f"Total books remaining: {books.count()}")