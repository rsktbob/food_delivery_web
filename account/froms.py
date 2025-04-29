from models import BaseUser
from django.contrib.auth.forms import UserCreationForm
from django import forms

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class CustomerRegisterForm(BaseRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        if commit:
            user.save()
        return user

class VendorRegisterForm(BaseRegisterForm):
    company_name = forms.CharField(max_length=100, required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'
        if commit:
            user.save()
        return user

class CourierRegisterForm(BaseRegisterForm):
    vehicle_type = forms.CharField(max_length=50, required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'courier'
        if commit:
            user.save()
        return user