from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Email_Bot(models.Model):
    # Connects a user to this bot. If user is deleted, bot is deleted.
    creator = models.ForeignKey(User, on_delete=models.CASCADE) 

    sender = models.CharField(max_length=50)
    email_password = models.CharField(max_length=40, default='Default_password')
    from_email = models.CharField(max_length=50)
    to_email = models.CharField(max_length=50)
    subject = models.CharField(max_length=150)
    email_content = models.TextField()
    response = models.TextField()
    
    def get_absolute_url(self):
        return reverse('form-home')