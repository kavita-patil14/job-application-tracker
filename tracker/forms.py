from django import forms
from .models import JobApplication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["company_name", "job_title", "status", "job_link","deadline"]
        widgets = {
            "applied_date": forms.DateInput(attrs={"type": "date"}),
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = "Required. Letters, digits and @/./+/-/_ only."

        self.fields['password1'].help_text = mark_safe("""
               <ul>
                   <li>Minimum 8 characters</li>
                   <li> Not too similar to personal info</li>
                   <li>Cannot be entirely numeric.</li>
                   <li>Not a common password</li>
               </ul>
           """)
        self.fields['password2'].help_text = "Re-enter the same password."

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

