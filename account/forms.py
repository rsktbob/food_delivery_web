from django import forms
from django.contrib.auth.hashers import make_password
from account.models import BaseUser, CustomerProfile, VendorProfile, CourierProfile

# Base form with common fields and methods
class BaseRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password manually since we're not using UserCreationForm
        user.password = make_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user

class CustomerRegisterForm(BaseRegisterForm):
    save_address = forms.CharField(max_length=255, required=True)
    default_payment_method = forms.CharField(max_length=20, required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        
        if commit:
            user.save()
            customer_profile = CustomerProfile(
                user=user,
                save_address=self.cleaned_data['save_address'],
                default_payment_method=self.cleaned_data['default_payment_method']
            )
            customer_profile.save()
        
        return user

class VendorRegisterForm(BaseRegisterForm):
    restaurant_name = forms.CharField(max_length=100, required=True)
    restaurant_address = forms.CharField(max_length=255, required=True)
    restaurant_license_number = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=500, required=False)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'
        
        if commit:
            user.save()
            vendor_profile = VendorProfile(
                user=user,
                restaurant_name=self.cleaned_data['restaurant_name']
                # Add other fields as needed
            )
            vendor_profile.save()
        
        return user

class CourierRegisterForm(BaseRegisterForm):
    vehicle_type = forms.CharField(max_length=20, required=True)
    license_plate = forms.CharField(max_length=20, required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'courier'
        
        if commit:
            user.save()
            courier_profile = CourierProfile(
                user=user,
                vehicle_type=self.cleaned_data['vehicle_type'],
                license_plate=self.cleaned_data['license_plate']
            )
            courier_profile.save()
        
        return user