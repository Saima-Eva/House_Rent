from django import forms
from .models import toLet_model

class ToLetModelForm(forms.ModelForm):
    class Meta:
        model = toLet_model
        fields = ['rent_title', 'location', 'homeDescription', 'rentDescription', 'deadline', 'nid', 'homePicture']
