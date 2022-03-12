from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):

    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(CommentForm, self).__init__(*args, **kwargs)
    #    self.fields['name'].widget.attrs['readonly'] = True
    #    self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = Comment
        # fields = ('name', 'email', 'body')
        fields = ('body',)


class SearchForm(forms.Form):
    query = forms.CharField()


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body')