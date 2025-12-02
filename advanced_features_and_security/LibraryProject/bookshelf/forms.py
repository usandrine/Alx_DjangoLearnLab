"""
Forms for bookshelf app with security best practices.
Task 2: Secure form handling.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.text import slugify
import re
from .models import Book, Author

class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form handling.
    Includes CSRF protection, input validation, and sanitization.
    """
    
    # Secure form fields with validation
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Your Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        required=True,
        label='Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        })
    )
    
    age = forms.IntegerField(
        required=True,
        label='Age',
        min_value=1,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
    )
    
    def clean_name(self):
        """Sanitize and validate name field"""
        name = self.cleaned_data['name']
        
        # Strip HTML tags to prevent XSS
        name = strip_tags(name)
        
        # Remove any potentially dangerous characters
        name = re.sub(r'[<>"\'&;]', '', name)
        
        # Validate length
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
        if len(name) > 100:
            raise ValidationError('Name must be less than 100 characters.')
        
        return name
    
    def clean_message(self):
        """Sanitize and validate message field"""
        message = self.cleaned_data['message']
        
        # Strip HTML tags to prevent XSS
        message = strip_tags(message)
        
        # Remove script tags and event handlers
        message = re.sub(r'<script.*?>.*?</script>', '', message, flags=re.IGNORECASE)
        message = re.sub(r'on\w+=".*?"', '', message)
        
        # Validate length
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')
        
        if len(message) > 1000:
            raise ValidationError('Message must be less than 1000 characters.')
        
        return message
    
    def clean(self):
        """Additional cross-field validation"""
        cleaned_data = super().clean()
        
        # Example: Validate that age is appropriate for certain names
        name = cleaned_data.get('name')
        age = cleaned_data.get('age')
        
        if name and age:
            # Simple validation example
            if age < 18 and 'admin' in name.lower():
                raise ValidationError('Admin users must be at least 18 years old.')
        
        return cleaned_data


class BookForm(forms.ModelForm):
    """Secure book form with validation"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def clean_title(self):
        """Sanitize book title"""
        title = self.cleaned_data['title']
        title = strip_tags(title)
        title = re.sub(r'[<>"\'&;]', '', title)
        return title
    
    def clean_description(self):
        """Sanitize book description"""
        description = self.cleaned_data.get('description', '')
        description = strip_tags(description)
        description = re.sub(r'<script.*?>.*?</script>', '', description, flags=re.IGNORECASE)
        return description
    
    def clean_isbn(self):
        """Validate ISBN format"""
        isbn = self.cleaned_data.get('isbn', '')
        if isbn:
            # Remove hyphens and spaces
            isbn = isbn.replace('-', '').replace(' ', '')
            
            # Validate ISBN-10 or ISBN-13 format
            if len(isbn) == 10:
                # Validate ISBN-10
                if not re.match(r'^\d{9}[\dX]$', isbn):
                    raise ValidationError('Invalid ISBN-10 format.')
            elif len(isbn) == 13:
                # Validate ISBN-13
                if not re.match(r'^\d{13}$', isbn):
                    raise ValidationError('Invalid ISBN-13 format.')
            else:
                raise ValidationError('ISBN must be 10 or 13 digits.')
        
        return isbn


class SearchForm(forms.Form):
    """Secure search form with parameterized queries"""
    
    query = forms.CharField(
        max_length=100,
        required=True,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('author', 'Author'),
            ('isbn', 'ISBN'),
        ],
        initial='title',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean_query(self):
        """Sanitize search query"""
        query = self.cleaned_data['query']
        query = strip_tags(query)
        query = re.sub(r'[<>"\'&;]', '', query)
        return query