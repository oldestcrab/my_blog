from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import LikeCount, LikeRecord

def success_response(liked_num):
    # 点赞成功返回的数据
    data = {
        'status': 'SUCCESS',
        'liked_num': liked_num,
    }
    return JsonResponse(data)

def error_response(message):
    # 点赞失败返回的数据
    data = {
        'status': 'ERROR',
        'message': message,
    }
    return JsonResponse(data)

def like_change(request):
    """
    更改点赞状态视图
    :param request:
    :return:
    """
    user = request.user
    if not user.is_authenticated:
        return error_response('尚未登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_response('点赞对象不存在')

    #  判断是点赞还是取消点赞
    if request.GET.get('is_like') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 点赞总数+1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return success_response(like_count.like_num)
        else:
            return error_response('您已赞过')
    else:
        # 先判断是否点赞过
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 取消点赞
            like_record =  LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 如果已有数据，点赞总数-1，否则报错
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.like_num -= 1
                like_count.save()
                return success_response(like_count.like_num)
            else:
                return error_response('数据错误')
        else:
            return error_response('您没有点赞过')