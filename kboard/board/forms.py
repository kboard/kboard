from django import forms
from django_summernote.widgets import SummernoteWidget
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'id': 'id_new_post_title', 'class': 'form-control', 'name': 'post_title_text', 'placeholder': 'Insert Title'}),
            'content': SummernoteWidget(),
        }
