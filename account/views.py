from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View 
from account.forms import CustomerRegisterForm, VendorRegisterForm, CourierRegisterForm

class RegisterView(View):
    user_type = None  # 透過 URL 傳入的參數

    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')  # 從 URL 抓取參數

        if user_type == 'customer':
            form = CustomerRegisterForm(request.POST)
        elif user_type == 'vendor':
            form = VendorRegisterForm(request.POST)
        elif user_type == 'courier':
            form = CourierRegisterForm(request.POST)
        else:
            messages.error(request, "Invalid user type")
            return redirect('register')

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'account/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    
    def form_valid(self, form):
        # First execute parent login logic
        response = super().form_valid(form)
        
        # Redirect based on user type
        user = self.request.user
        if user.is_customer():
            return redirect('customer_dashboard')
        elif user.is_vendor():
            return redirect('vendor_dashboard')
        elif user.is_courier():
            return redirect('courier_dashboard')
        else:
            logout(self.request)
            messages.error(self.request, 'Invalid user type')
            return redirect('login')
        
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please check your username and password.')
        return super().form_invalid(form)