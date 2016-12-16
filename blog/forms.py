from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class SortItemsBy(forms.Form):

    class Meta:
        sorted = forms.CharField(max_length=15)