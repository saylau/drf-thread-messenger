from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .users.views import UserViewSet, UserCreateViewSet
from .chat.urls import urlpatterns as chat_urlpatterns
from .users.urls import urlpatterns as users_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(users_urlpatterns)),
    path('chat/', include(chat_urlpatterns)),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
