from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import BaseUser, CustomerProfile, CourierProfile, VendorProfile

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class CustomerRegisterForm(BaseRegisterForm):
    save_address = forms.CharField(max_length=255)
    default_payment_method = forms.CharField(max_length=20, required=False)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                save_address=self.cleaned_data['save_address'],
                default_payment_method=self.cleaned_data['default_payment_method'],
            )
        return user

class VendorRegisterForm(BaseRegisterForm):
    restaurant_name = forms.CharField(max_length=100, required=True)
    bank_account_details = forms.CharField(required=False)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'
        if commit:
            user.save()
            VendorProfile.objects.create(
                user=user,
                bank_account_details = self.cleaned_data['bank_account_details'],
                restaurant_name = self.cleaned_data['restaurant_name'],
            )
        return user

class CourierRegisterForm(BaseRegisterForm):
    vehicle_type = forms.CharField(max_length=50, required=True)
    license_plate = forms.CharField(max_length=20, required=False)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'courier'
        if commit:
            user.save()
            CourierProfile.objects.create(
                user=user,
                vehicle_type=self.cleaned_data['vehicle_type'],
                license_plate=self.cleaned_data['license_plate']
            )
        return user