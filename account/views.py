<<<<<<< Updated upstream
from django.shortcuts import render
=======
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View 
from account.forms import CustomerRegisterForm, VendorRegisterForm, CourierRegisterForm
>>>>>>> Stashed changes

# Create your views here.