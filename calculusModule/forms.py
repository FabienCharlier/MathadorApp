from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
import django.forms as forms
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from . import models

class LoginForm(forms.Form):
    email = forms.EmailField(label="Entrez votre email")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not DjangoUser.objects.filter(email=email).exists():
            raise ValidationError("Adresse email inconnue, veuillez essayer avec une autre adresse email ou contacter l'administrateur pour créer un compte")
        return email
    
class AddScoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddScoreForm, self).__init__(*args, **kwargs)
        for visibleInput in self.visible_fields():
            visibleInput.field.widget.attrs['class'] = 'scoreInput'

    class Meta:
        model = models.Score
        fields = ('numericScore', 'nullScoresPercentage', 'mathadorsPercentage')

class NewWeekMailForm(forms.Form):
    currentNumbers = forms.CharField(label="Tirage de la semaine", max_length=100)
    personnalizedText = forms.CharField(label="Texte personnalisé", widget=forms.Textarea(attrs={"rows":"5"}))

class ResultsMailForm(forms.Form):
    personnalizedText = forms.CharField(label="Texte personnalisé", widget=forms.Textarea(attrs={"rows":"5"}))