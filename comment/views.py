from django.http import JsonResponse
from django.shortcuts import render

from .forms import CommentForm
from .models import Comment

def comment_update(request):
    """
    评论更新视图
    :param request:
    :return: 错误信息或者异步刷新评论
    """
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
        # 测试顶级评论和父辈评论是否一致，新评论ajax提交

        data = {
            'status': 'SUCCESS',
            'obj': comment_form.cleaned_data['content_object'],
        }
        # 成功则异步刷新数据
        return render(request, 'share_layout/comment_refresh.html', context=data)
    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0],
        }
        # 失败则返回错误信息
        return JsonResponse(data)
