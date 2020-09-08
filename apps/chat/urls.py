from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import GetThreadView, ThreadView, UsernameListView

urlpatterns = [
    path('<str:thread_id>/', ThreadView, name='thread'),
    path('', UsernameListView, name='username_list'),
    path('get_thread/<str:username>', GetThreadView.as_view(), name='get_thread')
]
