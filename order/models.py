from django.db import models
from account.models import CustomerProfile, CourierProfile, VendorProfile
from Restaurant.models import Restaurant, MenuItem

class Cart(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='cart')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.username}'s Cart"
    
    def clear(self):
        self.cartitem_set.all().delete()
        self.restaurant = None
        self.save()
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    def get_total_price(self):
        item_price = self.menu_item.price
        # customizations_price = sum(c.choice.additional_price for c in self.cartitemcustomization_set.all())
        return item_price * self.quantity
    
    def save(self, *args, **kwargs):
        existing_item = CartItem.objects.filter(cart=self.cart, menu_item=self.menu_item).first()

        if existing_item:
            CartItem.objects.filter(pk=existing_item.pk).update(
                quantity=existing_item.quantity + self.quantity
            )
            print(existing_item.quantity, self.quantity)
        else:
            super().save(*args, **kwargs)

    

# class CartItemCustomization(models.Model):
#     cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
#     choice = models.ForeignKey(CustomizationChoice, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.cart_item.menu_item.name} - {self.choice.name}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('Created', 'Created'), # 這是顧客創建訂單時，order為created
        ('Accepted', 'Confirmed by Restaurant'),#餐廳接受
        ('Assigned', 'Assigned to Courier'),#有外送員接單
        ('Picked_Up', 'Picked Up'),#外送員拿到餐點
        ('Finish', 'Finish'),#外送員送到餐點
    )

    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    courier = models.ForeignKey(CourierProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Created')
    payment_method = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"
    
    def calculate_totals(self):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.grand_total = self.total_price + self.delivery_fee
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    def get_total_price(self):
        # customizations_price = sum(c.additional_price for c in self.orderitemcustomization_set.all())
        return self.unit_price * self.quantity

# class OrderItemCustomization(models.Model):
#     order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='customizations')
#     option_name = models.CharField(max_length=100)
#     choice_name = models.CharField(max_length=100)
#     additional_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
#     def __str__(self):
#         return f"{self.order_item.menu_item.name} - {self.choice_name}"