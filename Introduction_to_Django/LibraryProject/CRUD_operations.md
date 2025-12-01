# CRUD Operations Documentation

## Create Operation
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created: {book.title} by {book.author}")
`` `
Created: 1984 by George Orwell

## Retrieve Operation
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
`` `
Title: 1984, Author: George Orwell, Year: 1949

## Update Operation
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title to: {book.title}")
`` `
Updated title to: Nineteen Eighty-Four

## Delete Operation
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