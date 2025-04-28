from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Created', 'Created'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    courier = models.ForeignKey('Courier', on_delete=models.CASCADE, null=True, blank=True, related_name='deliveries')
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField('ShoppingCart', on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)

class ShoppingCart(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Abandoned', 'Abandoned'),
        ('Converted', 'Converted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Cart {self.id} - {self.status}"

    def save(self, *args, **kwargs):
        # Update modified date on every save
        self.modified_date = timezone.now()
        super().save(*args, **kwargs)

class FoodItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.IntegerField()
    category = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, related_name='cart_items')
    food = models.ForeignKey('FoodItem', on_delete=models.CASCADE, related_name='cart_items')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True, related_name='order_items')
    quantity = models.IntegerField(default=1)
    unit_price = models.IntegerField()
    added_date = models.DateTimeField(default=timezone.now)
    special_instructions = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.food.name}"
    
    @property
    def total_price(self):
        """Calculate the total price based on quantity and unit price"""
        return self.quantity * self.unit_price
    
    class Meta:
        # You might want to add some custom metadata
        ordering = ['-added_date']

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    formatted_address = models.TextField(blank=True, null=True)