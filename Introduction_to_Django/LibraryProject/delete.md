```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")
books = Book.objects.all()
print(f"Total books remaining: {books.count()}")
`` `
Book deleted successfully
Total books remaining: 0