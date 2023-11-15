from django import forms 
from .models import Comment
from .models import Movie

class CommentForm(forms.ModelForm): 
    class Meta:
        model = Comment
        fields = ("comment",)

class MovieSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)