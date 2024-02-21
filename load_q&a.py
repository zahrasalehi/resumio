import json
from django.core.management.base import BaseCommand
from resumio.thisIsWhereUShouldTakeAlook.models import ChatHistory


class Command(BaseCommand):
    help = 'Load Fake data from JSON file'

    def handle(self, *args, **options):
        with open('fake_chat.json', 'r') as file:
            data = json.load(file)
            for entry in data:
                ChatHistory.objects.create(user_input=entry['user_input'], answer=entry['answer'])

        self.stdout.write(self.style.SUCCESS('Successfully loaded fake data.'))
