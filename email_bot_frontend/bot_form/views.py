from django.shortcuts import render
from django.http import HttpResponse

bot_data = [
        "devinhimmelheber@gmail.com",
        "devinhimmelheber1@gmail.com",
        "What up fuckers?!",
        "That's right, dummy data for the win!",
]
to_email = "devinhimmelheber@gmail.com"
from_email = "devinhimmelheber1@gmail.com"
subject = "What up fuckers?!"
body_text = "That's right, dummy data for the win!"

# Create your views here.
def home(request):
    context = {
        'data': bot_data
    }
    return render(request, 'bot_form/form.html', context)