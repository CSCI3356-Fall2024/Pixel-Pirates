from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Profile, Campaign, News
from .choices import SCHOOL_CHOICES, MAJOR_CHOICES, MINOR_CHOICES

class ProfileForm(forms.ModelForm):
    school = forms.ChoiceField(choices=SCHOOL_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    # Graduation year dropdown with the default year set to the next year
    current_year = datetime.now().year
    YEAR_CHOICES = [('', 'Select Year')] + [(year, year) for year in range(current_year, current_year + 10)]
    graduation_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=current_year + 1,  # Default to the next year
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Profile
        fields = ['name', 'school', 'major',
            'minor', 'graduation_year', 'picture', 'bio']

        widgets = {
            'major': forms.SelectMultiple(attrs={
                'class': 'form-control multiselect-target'
            }),
            'minor': forms.SelectMultiple(attrs={
                'class': 'form-control multiselect-target'
            }),
        }

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'title', 'description', 'date_begin', 'date_end',
            'time_begin', 'time_end', 'points', 'news', 
            'validation', 'location'
        ]
        widgets = {
            'location': forms.SelectMultiple(attrs={
                'class': 'form-control multiselect-target' 
            }),
            'date_begin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_begin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'validation': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_begin = cleaned_data.get('date_begin')
        date_end = cleaned_data.get('date_end')

        # Validate that the end date is not before the start date
        if date_begin and date_end and date_end < date_begin:
            raise ValidationError("End date must be on or after the start date.")

        return cleaned_data
    
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['display_title', 'external_url', 'news_image', 
                  'date_begin', 'date_end', 'time_begin', 'time_end']
        widgets = {
            'date_begin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_begin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        display_title = forms.CharField(required=True)
        external_url = forms.CharField(required=True)
        
    def clean(self):
        cleaned_data = super().clean()
        date_begin = cleaned_data.get('date_begin')
        date_end = cleaned_data.get('date_end')

        # Validate that the end date is not before the start date
        if date_begin and date_end and date_end < date_begin:
            raise ValidationError("End date must be on or after the start date.")

        return cleaned_data