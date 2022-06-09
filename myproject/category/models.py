from tkinter import CASCADE
from django.db import models
from django.urls import reverse


class Category(models.Model):
    cat_name= models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    cat_image = models.ImageField(upload_to ='media/category', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('product_by_category', args=[self.slug])

    def __str__(self):
        return self.cat_name 


class SubCategory(models.Model):
    cat_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcat_name =models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    subcat_image = models.ImageField(upload_to ='media/subcategory', blank=True)

    

    def __str__(self):
        return self.subcat_name


class SubSubCategory(models.Model):
    subcat_name = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null = True)
    subsubcat_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    subsubcat_image = models.ImageField(upload_to = 'media/subsubcategory', blank=True)

    class Meta:
        verbose_name = 'subsubcategory'
        verbose_name_plural = 'subsubcategories'
	
    def __str__(self):
        return self.subsubcat_name
