from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
<<<<<<< HEAD
<<<<<<< Updated upstream
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
=======
    path('login/', views.CustomLoginView.as_view(template_name="./account/login.html"), name="login"),
>>>>>>> Stashed changes
=======
    path('login/', views.CustomLoginView(template_name="./account/login.html"), name="login"),
>>>>>>> main
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('register/<str:user_type>/', views.register, name="register"),   
]
