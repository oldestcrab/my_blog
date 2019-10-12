from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType

from .forms import CommentForm
from .models import Comment

def comment_update(request):
    comment_form = CommentForm(request.POST, user=request.user)
    # 判断数据是否合法
    if comment_form.is_valid():
        comment = Comment()
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.content = comment_form.cleaned_data['content']
        comment.user = request.user
        parent = comment_form.cleaned_data['parent']
        # 如果有父辈评论
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        data = {
            'username': comment.user.get_nickname_or_username(),
            'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'comment_content': comment.content,
            'content_type': ContentType.objects.get_for_model(comment).model,
            'status': 'SUCCESS',
            'pk': comment.pk,
            'root_pk': comment.root.pk if comment.root else '',
        }

        if parent:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0],
        }
    return JsonResponse(data)