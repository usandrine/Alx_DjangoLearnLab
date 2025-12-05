from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django_blog.blog.models import Post

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            }),
        }
    
        def clean_content(self):
            content = self.cleaned_data.get('content')
            if len(content.strip()) < 1:
                raise forms.ValidationError("Comment cannot be empty.")
            return content
    
    class PostForm(forms.ModelForm):
        tags = forms.CharField(required=False, help_text="Comma-separated tags")
    
        class Meta:
            model = Post
            fields = ['title', 'content', 'tags']
    
        def save(self, commit=True):
            post = super().save(commit=False)
            if commit:
                post.save()
                self.save_m2m()  # Save tags
            return post