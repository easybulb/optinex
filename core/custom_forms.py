from django import forms
from .models import UserProfile

class CustomSignupForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    def save(self, request):
        # Import SignupForm inside the method to avoid circular import
        from allauth.account.forms import SignupForm
        
        # Call the parent save method to save the user
        user = SignupForm.save(self, request)
        
        # Create a UserProfile instance and save the phone number
        UserProfile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user

    def signup(self, request, user):
        # Called by allauth during signup
        UserProfile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
