from django import forms
from datetime import datetime
from .models import Profile

class ProfileForm(forms.ModelForm):
    SCHOOL_CHOICES = [
        ('CSOM', 'Carroll School of Management'),
        ('MCAS', 'Morrissey College of Arts and Sciences'),
        ('LSEHD', 'Lynch School of Education and Human Development'),
        ('CSON', 'Connell School of Nursing'),
        ('LAW', 'Boston College Law School'),
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
        fields = ['username', 'name', 'bc_email', 'school', 'major1', 'major2',
            'minor1', 'minor2', 'graduation_year', 'picture']
        
        def clean_bc_email(self):
            bc_email = self.cleaned_data.get('bc_email')

            if not bc_email.endswith('@bc.edu'):
                raise forms.ValidationError("Please enter a valid BC email address.")

            if Profile.objects.filter(bc_email=bc_email).exists():
                raise forms.ValidationError("This email is already associated with another account.")
            
            return bc_email