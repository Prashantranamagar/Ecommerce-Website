from unicodedata import category
from django.http import HttpResponse
from numpy import product
from category.models import Category, SubCategory, SubSubCategory
from products.models import Products

from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.db.models import Q

def home(request):
    products = Products.objects.all()
    category =  Category.objects.all()
    subcategory = SubCategory.objects.all()
    subsubcategory = SubSubCategory.objects.filter()


    return render(request, 'myproject/home.html', {
        'products':products, 
        'category':category, 
        'subcategory':subcategory, 
        'subsubcategory':subsubcategory
        })

#making same function for the "store" url and store/<slug:cat_slug> url.
def store(request, cat_slug=None):
    product=None
    if cat_slug != None:
        product = Products.objects.filter(category__subcat_name__slug=cat_slug, is_available = True) #
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        count = product.count()

    
    else:
        product = Products.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        count = product.count()


    return render(request, 'myproject/store.html', {
        'product':paged_product,
        'count':count,
        

    })

#or u can make seprate view without for the url with slug
# def cat_product(request, cat_slug):
#     product = Products.objects.filter(subcategory__slug = cat_slug, is_available=True)
#     count = product.count()
#     return render(request, 'myproject/store.html', {
#         'product':product,
#         'count':count,
#     })

 
def search(request):
    keyword = request.GET['search']
    if keyword:
        product = Products.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)) 
        # if we put comma it acts as and operator so we put | or operator ie it shows result if one of them is true.
    return render(request, 'myproject/store.html', {
        'product':product
    })