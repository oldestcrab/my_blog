from django.shortcuts import render

# Create your views here.
def my_notifications(request):
    return render(request, 'my_notifications/my_notifications.html',)