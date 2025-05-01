from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import WorkSchedule
from django.contrib.auth.forms import AuthenticationForm

class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ['event_type', 'start_date', 'end_date', 'start_time', 'end_time']
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Username
        self.fields['username'].label = 'Name'  # ✅ Rename label
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your name'
        self.fields['username'].help_text = ''
        # Email
        self.fields['email'].label = 'Email Address'  # ✅ Rename label
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email Address'
        self.fields['email'].help_text = ''
        # Password1
        self.fields['password1'].label = 'Password'  # ✅ Rename label
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your Password'
        self.fields['password1'].help_text = ''
        # Password2
        self.fields['password2'].label = 'Password Confirmation'  # ✅ Rename label
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].help_text = ''
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Remember Me")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Name'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your name',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })

        self.fields['remember_me'].widget.attrs.update({
            'class': 'form-check-input',
        })