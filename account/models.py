from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
USER_TYPES = (
    ('customer', 'Customer'),
    ('courier', 'Courier'),
    ('vendor', 'Vendor'),
)

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
class User(AbstractUser):
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

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.address_line1}, {self.city}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    favorite_restaurants = models.ManyToManyField('restaurants.Restaurant', blank=True, related_name='favorited_by')
    saved_addresses = models.ManyToManyField(Address, blank=True, related_name='saved_by_customers')
    default_payment_method = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"Customer: {self.user.username}"

class CourierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courier_profile')
    is_available = models.BooleanField(default=False)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=20, blank=True)
    license_plate = models.CharField(max_length=20, blank=True)
    id_verification_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Courier: {self.user.username}"

class VendorProfile(models.Model):
<<<<<<< Updated upstream
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=255)
    business_registration_number = models.CharField(max_length=50, blank=True)
    tax_identification_number = models.CharField(max_length=50, blank=True)
    verification_status = models.BooleanField(default=False)
    bank_account_details = models.TextField(blank=True)
=======
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='vendor_profile')
    bank_account_details = models.CharField(blank=True)
    restaurant_name = models.CharField(max_length=20)
>>>>>>> Stashed changes
    
    def __str__(self):
        return f"Vendor: {self.business_name}"