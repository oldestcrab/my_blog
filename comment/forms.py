from django import forms
from django.contrib.contenttypes.models import ContentType

from ckeditor.widgets import CKEditorWidget

from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.CharField(widget=forms.HiddenInput)
    text = forms.CharField(label=False, widget=CKEditorWidget(config_name='comment_ckeditor'))
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))