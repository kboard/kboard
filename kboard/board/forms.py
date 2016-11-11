from django import forms
from django.forms.utils import ErrorList
from django_summernote.widgets import SummernoteWidget

from .models import Post, Attachment

EMPTY_TITLE_ERROR = "제목을 입력하세요"
EMPTY_CONTENT_ERROR = "내용을 입력하세요"


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="form-group has-error">%s</div>' % ''.join(['<div class="help-block">%s</div>' % e for e in self])


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'file')
        widgets = {
            'title': forms.TextInput(attrs={'id': 'id_post_title', 'class': 'form-control', 'placeholder': 'Insert Title'}),
            'content': SummernoteWidget(),
        }
        error_messages = {
            'title': {'required': EMPTY_TITLE_ERROR},
            'content': {'required': EMPTY_CONTENT_ERROR}
        }

    def __init__(self, *args, **kwargs):
        kwargs_new = {'error_class': DivErrorList}
        kwargs_new.update(kwargs)
        super(PostForm, self).__init__(*args, **kwargs_new)


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('attachment', )
