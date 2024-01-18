from django.db import models


class ChatHistory(models.Model):
    user_input = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
