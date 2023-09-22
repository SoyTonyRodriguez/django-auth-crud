# ModelForm: es una forma conveniente de generar formularios basados en los modelos de la base de datos
from django.forms import ModelForm

# Para dar estilo
from django import forms

# Task: Modelo que hemos creado de la base de datos
from .models import Task


# Heredamos de ModelForm, es decir tendremos todas sus funcionalidades
class Task_Form(ModelForm):
    # Meta: Clase interna que se utiliza para proporcionar metadatos sobre el formulario.
    class Meta:
        model = Task

        # Describiendo las campos que serán incluidos en el formulario
        fields = ["title", "description", "important"]

        # Para dar estilo a un formulario propio desde la clase
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Write a title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Write a description"}
            ),
            "important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
