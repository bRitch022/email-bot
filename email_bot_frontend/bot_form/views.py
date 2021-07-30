from django.shortcuts import render
from .models import Email_Bot
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    context = {
        'bots': Email_Bot.objects.all()
    }
    return render(request, 'bot_form/form.html', context)

class BotListView(LoginRequiredMixin, ListView):
    model = Email_Bot
    template_name = 'bot_form/form.html'
    context_object_name = 'bots'

class BotCreateView(LoginRequiredMixin, CreateView):
    model = Email_Bot
    fields = ['sender', 'email_password', 'from_email', 'to_email', 'subject', 'email_content', ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        # Create email bot here
        return super().form_valid(form)

class BotUpdateView(LoginRequiredMixin, UpdateView):
    model = Email_Bot
    fields = ['sender', 'email_password', 'from_email', 'to_email', 'subject', 'email_content', ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        # Update email bot here
        return super().form_valid(form)