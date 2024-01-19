from django.urls import path
from .views import *

urlpatterns = [
    path(r'', get_question, name='chat-view'),
    path(r'get/', get_answer, name='answer-view'),

]
