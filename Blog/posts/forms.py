from django import forms
from .models import Comment

class EmailPostForm(forms.Form):

    def __init__(self, *args, **kwargs):
       super(EmailPostForm, self).__init__(*args, **kwargs)
       self.fields['name'].widget.attrs['readonly'] = True
       self.fields['email'].widget.attrs['readonly'] = True

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com'}))
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
