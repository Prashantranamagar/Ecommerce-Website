import decimal
from django.db import models
from numpy import product
from category.models import SubSubCategory, SubCategory, Category
from django.contrib.auth.models import User


class Products(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=50, decimal_places=3)
    images = models.ImageField(upload_to ='media/products', blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(SubSubCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(default='abc')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True) 
    stock = models.IntegerField(default=1)

    #Notes
    #for query subcategory is not needed we can get subcategory items and categoryitems from the SubSubCategory foreign key
    #to get SubSubcategory item foreignkeyname__subsubcategoryitemname 
    #to get Subcategory item foreignkeyname__subsubcategoryforeignkeyname__subcategoryitemname
    #to get Category item foreignkeyname__subsubcategoryforeignkeyname__subcategoryforeignkey_subcategoryitemname
    #we can query in reverse order to from category to subcategory to subsubcategory to product
    # we ca query in circle to

    #in template use . in place of __


    def __str__(self):
        return self.product_name



class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)



variation_category_choices = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=225, choices=variation_category_choices)
    variation_value = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    objects = VariationManager()


class ReviewRating(models.Model):
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject    


class ProductGallery(models.Model):
    product =models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media', max_length=255)

    def __str__(self):
        return self.product.product_name

    verbose_name = 'productgallery'
    verbose_name_plural = 'productgallery'