from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'graduation_year', 'major1', 'major2', 'picture']