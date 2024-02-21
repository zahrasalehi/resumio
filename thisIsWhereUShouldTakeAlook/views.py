from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import openai
from .models import ChatHistory
from resumio import settings


def get_question(request):
    query = request.GET.get('user_input', '')

    # Call OpenAI GPT API
    # openai.api_key = settings.OPENAI_API_KEY
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=user_input,
    #     max_tokens=100
    # )
    answer = ChatHistory.objects.filter(user_input__icontains=query)
    # Save chat history
    return render(request, '../templates/thisIsWhereUShouldTakeAlook/resume_page.html',
                  {'query': query}, {'answer': answer})
# TODO: make html page better
