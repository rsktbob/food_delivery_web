from django.db import models
from django.contrib.auth.models import AbstractUser

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
