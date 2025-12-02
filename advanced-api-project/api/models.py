from django.db import models

class Author(models.Model):
    """Author model representing book authors"""
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Book(models.Model):
    """Book model representing published books"""
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    in_stock = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'author']