from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# # Create your models here.
# class BaseUser(AbstractUser):
#     # 基礎用戶信息
#     user_type = models.CharField(
#         max_length=10,
#         choices=USER_TYPES,  # 設定 choices 來指定下拉選單選項
#         default='customer',  # 默認值
#     )

#     def __str__(self):
#         return self.username
    

# class CustomerProfile(BaseUser):
#     user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='customer_profile')
#     # 客戶特有字段


# class CourierProfile(BaseUser):
#     user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='courier_profile')
#     vehicle_type = models.CharField(max_length=50, blank=True, null=True)
#     available = models.BooleanField(default=False)
#     # 快遞員特有字段

# class VendorProfile(BaseUser):
#     user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='vendor_profile')
#     company_name = models.CharField(max_length=100)
#     business_license = models.CharField(max_length=50, blank=True, null=True)
#     # 供應商特有字段
class BaseUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('courier', 'Courier'),
        ('vendor', 'Vendor'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def is_customer(self):
        return self.user_type == 'customer'
    
    def is_courier(self):
        return self.user_type == 'courier'
    
    def is_vendor(self):
        return self.user_type == 'vendor'

class CustomerProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='customer_profile')
    save_address = models.CharField(max_length=255)
    default_payment_method = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"Customer: {self.user.username}"

class CourierProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='courier_profile')
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=20, blank=True)
    license_plate = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"Courier: {self.user.username}"

class VendorProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='vendor_profile')
    restaurant_name = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Vendor: {self.user.username}"