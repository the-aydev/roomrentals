from django.shortcuts import render, get_object_or_404
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import Message
from django.db.models import Q
import json
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def chatroom(request, pk: int):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(
        Q(receiver=request.user, sender=other_user)
    )
    messages.update(seen=True)
    messages = messages | Message.objects.filter(
        Q(receiver=other_user, sender=request.user))
    return render(request, "chat/chatroom1.html", {"other_user": other_user, 'users': User.objects.all(), "user_messages": messages})


@login_required
def ajax_load_messages(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False, receiver=request.user)

    print("messages")
    message_list = [{
        "sender": message.sender.full_name,
        "message": message.message,
        "sent": message.sender == request.user,
        "picture": other_user.photo.url,

        "date_created": naturaltime(message.date_created),

    } for message in messages]
    messages.update(seen=True)

    if request.method == "POST":
        message = json.loads(request.body)['message']

        m = Message.objects.create(
            receiver=other_user, sender=request.user, message=message)

        message_list.append({
            "sender": request.user.full_name,
            "full_name": request.user.full_name,
            "message": m.message,
            "date_created": naturaltime(m.date_created),

            "picture": request.user.photo.url,
            "sent": True,
        })
    print(message_list)
    return JsonResponse(message_list, safe=False)
