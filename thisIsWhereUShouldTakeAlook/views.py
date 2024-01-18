from django.shortcuts import render
from django.http import JsonResponse
import openai
from .models import ChatHistory
from resumio import settings


def chat_view(request):
    user_input = request.GET.get('user_input', '')

    # Call OpenAI GPT API
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=100
    )
    answer = response['choices'][0]['text']

    # Save chat history
    chat_history = ChatHistory.objects.create(
        user_input=user_input,
        answer=answer
    )

    return render(request, '../templates/thisIsWhereUShouldTakeAlook/resume_page.html',
                  {'user_input': user_input, 'answer': answer})
