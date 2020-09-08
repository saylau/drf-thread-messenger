from django.db import models

from apps.users.models import User


class Thread(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    users = models.ManyToManyField(User,related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
