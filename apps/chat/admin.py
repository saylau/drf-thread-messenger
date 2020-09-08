from django.contrib import admin

from .models import Message, Thread


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    pass
