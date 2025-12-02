```python
# Update the book title
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title to: {book.title}")

Updated title to: Nineteen Eighty-Four