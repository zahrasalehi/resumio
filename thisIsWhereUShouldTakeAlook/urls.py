from django.urls import path
from .views import *

urlpatterns = [
    path(r'post', get_question, name='chat-view'),

]
