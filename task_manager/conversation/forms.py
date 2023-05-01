from django.forms import ModelForm, Textarea, TextInput
from .models import Conversation

class SendMessageForm(ModelForm):
    class Meta:
        model = Conversation
        fields = ['message']
        widgets = {
            'message': Textarea(attrs={'type': 'text', 'class':'h-20 p-2 border-4 border-indigo-800 rounded-xl font-sans'})
        }