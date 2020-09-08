import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Thread, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = 'chat_%s' % self.thread_id

        # Join thread group
        async_to_sync(self.channel_layer.group_add)(
            self.thread_group_name,
            self.channel_name
        )

        self.accept()

        thread = Thread.objects.get(id=int(self.thread_id))
        messages = Message.objects.filter(thread=thread).order_by('created_at')
        for message in messages:
            self.send(text_data=json.dumps({
                'message': message.message,
                'username': self.user.username,
            })) 

    def disconnect(self, close_code):
        # Leave thread group
        async_to_sync(self.channel_layer.group_discard)(
            self.thread_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.user.username

        thread = Thread.objects.get(id=self.thread_id)
        Message.objects.create(author=self.user, message=message, thread=thread)
        # Send message to thread group
        async_to_sync(self.channel_layer.group_send)(
            self.thread_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from thread group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))