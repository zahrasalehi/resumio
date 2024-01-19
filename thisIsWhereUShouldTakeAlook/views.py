from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import openai
from .models import ChatHistory
from resumio import settings


def get_question(request):
    user_input = request.GET.get('user_input', '')

    # Call OpenAI GPT API
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=100
    )

    # Save chat history
    return render(request, '../templates/thisIsWhereUShouldTakeAlook/resume_page.html',
                  {'user_input': user_input})


# TODO: get answer in a separate function
def get_answer(request):
    answer = response['choices'][0]['text']
    # answer = 'this is test'
    return JsonResponse(answer)

# TODO: make a login required save function
# @login_required
# def save_resume(request):
#     chat_history = ChatHistory.objects.create(
#         user_input=user_input,
#         answer=answer
#     )

# TODO: make related html pages. like where to put about me and other stuff