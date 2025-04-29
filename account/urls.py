from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.CustomLoginView(template_name="./account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('register/<str:user_type>/', views.register, name="register"),   
]
