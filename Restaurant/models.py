from django.db import models
from account.models import VendorProfile

class Restaurant(models.Model):
    owner = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cuisine_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Food Categories"

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, related_name='menu_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class CustomizationOption(models.Model):
    OPTION_TYPE_CHOICES = (
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
    )
    
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='customization_options')
    name = models.CharField(max_length=100)
    option_type = models.CharField(max_length=10, choices=OPTION_TYPE_CHOICES)
    is_required = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.menu_item.name}"

class CustomizationChoice(models.Model):
    option = models.ForeignKey(CustomizationOption, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(max_length=100)
    additional_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.name} (+${self.additional_price})"