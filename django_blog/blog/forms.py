from django import forms
from taggit.forms import TagWidget
from taggit.models import Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=TagWidget(),  # Add TagWidget here
        help_text="Enter comma-separated tags"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Initialize tags for existing posts
            self.initial['tags'] = ", ".join(self.instance.tags.names())
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Clear existing tags and add new ones
            post.tags.clear()
            tag_names = self.cleaned_data['tags']
            if tag_names:
                for tag_name in tag_names.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        post.tags.add(tag_name)
        return post
    
    class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments using Django's ModelForm.
    Includes validation rules for comment content.
    """
    class Meta:
        model = Comment  # This specifies the model
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
    
    def clean_content(self):
        """Validation rule: Ensure comment is not empty and has minimum length."""
        content = self.cleaned_data.get('content')
        
        if not content or len(content.strip()) == 0:
            raise forms.ValidationError("Comment cannot be empty.")
        
        if len(content) > 1000:
            raise forms.ValidationError("Comment is too long. Maximum 1000 characters allowed.")
        
        return content