from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_customer():
            return render(request, 'home/customer_home.html')
        elif user.is_vendor():
            return render(request, 'home/vendor_home.html')
        elif user.is_courier():
            return render(request, 'home/courier_home.html')
        else:
            return render(request, 'home.html')
