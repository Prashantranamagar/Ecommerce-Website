from django.db import models
from django.contrib.auth.models import User

from products.models import Products, Variation


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    payment_id = models.CharField(max_length = 225)
    payment_method = models.CharField(max_length =255)
    amount_paid = models.CharField(max_length = 255)
    status = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'), 
        ('accepted', 'accepted'),
        ('Completed', 'Completed'), 
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    order_number = models.CharField(max_length =50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length = 50)
    phone = models.CharField(max_length = 50, null=True)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upadated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment =models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color =models.CharField(max_length=50)
    size =models.CharField(max_length=50)
    quantity =models.IntegerField()
    product_price =models.FloatField(max_length=50)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        self.product.product_name


