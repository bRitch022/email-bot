from django.urls import path
from .views import BotListView, BotCreateView, BotUpdateView
from . import views

urlpatterns = [
    path('', BotListView.as_view(), name='form-home'),
    path('create_bot/', BotCreateView.as_view(), name='bot-create'),
    #path('update_bot/<int:pk>', BotUpdateView.as_view(), name='bot-update'),
]