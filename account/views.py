from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View 
from account.forms import CustomerRegisterForm, VendorRegisterForm, CourierRegisterForm

def register(request):
    return render(request, './account/register.html')


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    
    def form_valid(self, form):
        # 先執行父類的登入邏輯
        super().form_valid(form)
        
        # 根據用戶類型重定向到不同頁面
        user = self.request.user
        if user.is_customer():
            return redirect('customer_dashboard')
        elif user.is_vendor():
            return redirect('vendor_dashboard')
        elif user.is_courier():
            return redirect('courier_dashboard')
        else:
            logout(self.request)
            
    
    def form_invalid(self, form):
        messages.error(self.request, '登入失敗，請檢查您的電子郵件和密碼')
        return super().form_invalid(form)
    

class CustomeRegisterView(View):
    def get(self, request, user_type):
        # 根據 user_type 顯示對應的註冊表單
        if user_type == 'customer':
            form = CustomerRegisterForm()
        elif user_type == 'courier':
            form = CourierRegisterForm()
        elif user_type == 'vendor':
            form = VendorRegisterForm()
        else:
            messages.error(request, "無效的職業類型")
            return redirect('login')
    

        # 將 user_type 傳遞給模板，讓表單根據職業進行顯示或處理
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, user_type):
        if user_type == 'customer':
            form = CustomerRegisterForm(request.POST)
        elif user_type == 'vendor':
            form = CourierRegisterForm(request.POST)
        elif user_type == 'courier':
            form = VendorRegisterForm(request.POST)
        form.save()

        messages.success(request, '註冊成功')
        return redirect('home')