from django.urls import path
from .views import *

urlpatterns = [
    path(r'', chat_view, name='chat-view'),
]
