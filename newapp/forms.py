from django import forms
from users.models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['title', 'content']