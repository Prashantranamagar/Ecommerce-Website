from sre_constants import SRE_FLAG_DEBUG
from django.shortcuts import render
from numpy import product
import products

from products.models import Products
from category.models import Category, SubCategory, SubSubCategory
from cart.models import Cart, CartItem
from cart.views import _cart_id


def product_detail(request, slug):
    try:
        products = Products.objects.get(slug=slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=products).exists()
    except Exception as e:
        raise e
    

    return render(request, 'myproject/product_detail.html', {
        'products':products, 
        'slug':slug,
        'in_cart': in_cart,
        })



