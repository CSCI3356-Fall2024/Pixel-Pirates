from django import forms
from datetime import datetime
from .models import Profile

class ProfileForm(forms.ModelForm):
    SCHOOL_CHOICES = [
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
        fields = ['name', 'bc_email', 'school', 'major',
            'minor', 'graduation_year', 'picture', 'bio']
        
        def clean_bc_email(self):
            bc_email = self.cleaned_data.get('bc_email')

            if not bc_email.endswith('@bc.edu'):
                raise forms.ValidationError("Please enter a valid BC email address.")

            if Profile.objects.filter(bc_email=bc_email).exists():
                raise forms.ValidationError("This email is already associated with another account.")
            
            return bc_email