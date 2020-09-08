from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.users.models import User

from .models import Message, Thread


def ThreadView(request, thread_id):
    return render(request, 'chat/thread_chat.html', {
        'thread_id': thread_id,
    })

def UsernameListView(request):
    usernames = list(User.objects.all().values_list('username', flat=True))

    return render(request, 'chat/chats_list.html', {
        'usernames': usernames,
    })


class GetThreadView(GenericAPIView):
    def get(self, request, username):
        author = request.user
        to = User.objects.get(username=username)

        thread = Thread.objects.filter(users__in=[author, to]).first()
        if not thread:
            thread = Thread.objects.create()
            thread.users.set([author, to])

        return redirect('thread', thread_id=thread.id)

