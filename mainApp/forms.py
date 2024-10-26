from django import forms
from datetime import datetime
from .models import Profile, Campaign

class ProfileForm(forms.ModelForm):
    SCHOOL_CHOICES = [
        ('', 'School'),
        ('CSOM', 'CSOM'),
        ('MCAS', 'MCAS'),
        ('LSEHD', 'LSEHD'),
        ('CSON', 'CSON'),
        ('LAW', 'LAW'),
    ]
    school = forms.ChoiceField(choices=SCHOOL_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    # Graduation year dropdown with the default year set to the next year
    current_year = datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(current_year, current_year + 10)]
    graduation_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=current_year + 1,  # Default to the next year
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Profile
        fields = ['name', 'school', 'major',
            'minor', 'graduation_year', 'picture', 'bio']

class CampaignForm(forms.ModelForm): 

    class Meta: 
        model = Campaign
        fields = ['title', 'description', 'date_begin', 'date_end', 'time_begin', 'time_end']
        widgets = {
            'date_begin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_begin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'time_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }