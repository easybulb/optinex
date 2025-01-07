from django import forms
from django.contrib.auth.models import User
from .models import Appointment, UserProfile

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone_number', 'service', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email



class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(required=False, max_length=15, label="Phone Number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')  # Get the user instance passed to the form
        super().__init__(*args, **kwargs)
        if hasattr(user, 'profile'):  # Ensure the profile exists
            self.fields['phone_number'].initial = user.profile.phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.phone_number = self.cleaned_data['phone_number']
                user.profile.save()
        return user
