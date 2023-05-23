from django.db import models
from products.models import Products, Variation
from django.contrib.auth.models import User


class Cart(models.Model):
    cart_id = models.CharField(max_length = 250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    variations =models.ManyToManyField(Variation, blank=True) 
    quantity = models.IntegerField(default=0, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name


