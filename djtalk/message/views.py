from django.shortcuts import render
from users.models import Users
from django.http import HttpResponse
from users.models import Messages


def add_message(request):
    if request.COOKIES.get('token'):
        sender = Users.objects.get(token=request.COOKIES.get('token'))
        m = Messages(
            text=request.POST['text'],
            sender=sender.id,
            receiver=request.POST['receiver']
        )
        m.save()
        return HttpResponse("Message Saved!")
    else:
        return HttpResponse('Please login first', status=403)


def chat(request, user_id=None):
    messages = []
    if request.COOKIES.get('token') and user_id:
        user = Users.objects.get(token=request.COOKIES.get('token'))
        messages = Messages.objects.filter(sender__in=[user.id, user_id], receiver__in=[user_id, user.id])
    print('user_id', user_id)
    return render(
        request,
        'chat.html',
        context={
            'users': Users.objects.all(),
            'receiver': user_id,
            'chat_available': user_id is not None,
            'messages': messages
        }
    )
