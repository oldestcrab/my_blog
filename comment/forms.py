from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from ckeditor.widgets import CKEditorWidget

from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(label=False, widget=CKEditorWidget(config_name='comment_ckeditor'))
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            # 获取对应的模型
            model_class = ContentType.objects.get(model=content_type).model_class()
            # 获取具体模型对象
            self.cleaned_data['content_object'] = model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        # 判断用户是否登录
        if not self.user.is_authenticated:
            raise forms.ValidationError('您尚未登录')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        """
        判断reply_comment_id是否合法
        :return:
        """
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id<0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id