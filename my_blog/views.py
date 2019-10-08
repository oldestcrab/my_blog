from django.shortcuts import render

def home(request):
    """
    主页视图
    :param request:
    :return:
    """
    context = {

    }
    return render(request, 'home.html', context=context)