from django import forms
from .models import *

class ShowItems(forms.ModelForm):
    class Meta:
        model = TodoApp
        fields = ["text"]
        labels = {"text": ""}
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2',
                                            "placeholder": "add your to-dos...",
                                            "id": 'todo-item'
                                            }),
        }
        