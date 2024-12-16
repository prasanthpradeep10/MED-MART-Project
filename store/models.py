from itertools import count
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.utils import timezone
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class Registration(models.Model):
    password = models.CharField(max_length=100, null=True)
    user_role = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_role
    


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='images/' , null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def get_most_common_rating(self):
        # Use 'rating' instead of 'value'
        most_common = self.ratings.values('rating').annotate(count=Count('rating')).order_by('-count', '-rating').first()
        return most_common['rating'] if most_common else None
    

   
    def __str__(self):
        return self.name
    
class DeliveryBoyStatus(models.Model):
    delivery_boy_update = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=10, choices=[('In', 'In'), ('Out', 'Out')], default='Out',null=True)
    last_updated = models.DateTimeField(auto_now=True,null=True)
    latitude = models.FloatField(null=True, blank=True)  # Latitude
    longitude = models.FloatField(null=True, blank=True)  # Longitude
    location_name = models.TextField(null=True, blank=True)
  

    def __str__(self):
        return f"{self.delivery_boy_update.username} - {self.status} (Last Updated: {self.last_updated})"


    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.TextField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Only keep one 'created_at'
    status = models.CharField(
        max_length=20,
        choices=[('Order Placed', 'Order Placed'), ('Pending', 'Pending'), ('shipped', 'shipped'), ('Out for Delivery', 'Out for Delivery') ,('Delivered', 'Delivered')],
        default='Order Placed',
        null=True,
    )
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_boy_update = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Add latitude field
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Add longitude field

    def save(self, *args, **kwargs):
        # Set the 'delivered_at' field when the status is set to 'Delivered'
        if self.status == 'Delivered' and not self.delivered_at:
            self.delivered_at = timezone.now()
        
        # Geocoding logic to find latitude and longitude
        if self.address and (not self.latitude or not self.longitude):  # Only geocode if address is present and lat/lon are missing
            try:
                geolocator = Nominatim(user_agent="myGeocoder")
                location = geolocator.geocode(self.address, timeout=10)  # Add a timeout to avoid infinite waiting
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                else:
                    print(f"Geocoding failed: Could not find coordinates for address: {self.address}")
            except GeocoderTimedOut:
                print("Geocoding timeout occurred. Try again later.")
        
        super().save(*args, **kwargs)


class Rating1(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  


    def __str__(self):
        return f"{self.user} - {self.product} - {self.rating} stars"
    
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1,null=True)

    def total_price(self):
        return self.product.price * self.quantity

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity}) in Order #{self.order.id}'
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", null=True)  # Add user ForeignKey
    address_line = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=100, null=True)
    is_default = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
    

  
    


   
    
    
    

     

    
        