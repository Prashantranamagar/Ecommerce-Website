from django.shortcuts import render
from category import models
from products.models import Products
from .models import SubCategory, Category, SubSubCategory



def category(request, cat_slug):
    product = Products.objects.filter(subcategory__cat_name__slug=cat_slug)
    count = product.count()
    
    return render(request, 'myproject/store.html', {
        'product':product ,
        'count':count,
    })


def subcategory(request, cslug, sslug):
    product = Products.objects.filter(subcategory__slug=sslug)
    count = product.count()
    return render(request, 'myproject/store.html', {'product':product, 'count':count})


def subsubcategory(request, cslug, sslug, ssslug):
    product = Products.objects.filter(category__slug=ssslug)
    count = product.count()
    return render(request, 'myproject/store.html', {'product':product, 'count':count})

