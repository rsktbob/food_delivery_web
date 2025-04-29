from django.urls import path

from marketplace import views


urlpatterns = [
    path('marketplace/', views.marketplace, name="marketplace"),
]