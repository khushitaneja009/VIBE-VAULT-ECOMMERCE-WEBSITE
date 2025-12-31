from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_cart_total(self):
        total = 0
        items = self.cartitem_set.all()  # Get all CartItem objects related to this Cart
        for item in items:
            total += item.get_total_price()  # Call the method in CartItem
        return total

    def __str__(self):
        return f"{self.user.username}'s Cart"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
