from django import forms
from django.forms import ModelForm
from .models import Message, Topic, Room

class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
    exclude = ['host', 'participants']
    

