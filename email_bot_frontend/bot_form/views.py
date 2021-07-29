from django.shortcuts import render
from .models import Email_Bot

# Create your views here.
def home(request):
    context = {
        'data': Email_Bot.objects.all()
    }
    return render(request, 'bot_form/form.html', context)