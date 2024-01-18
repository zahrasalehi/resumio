from django.urls import path
from .views import *

urlpatterns = [
    path(r'resume/', chat_view, name='chat-view'),
]
