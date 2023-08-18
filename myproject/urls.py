"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.http import HttpResponse 

def home(request):
    return HttpResponse("hello World")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    # path('', views.home, name="home"),
    path('category/', include('category.urls')),
    path('products/', include('products.urls')),
    path('account/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('store/', views.store, name='store'),
    path('store/<slug:cat_slug>', views.store, name='cat_product'),
    path('search/', views.search, name='search'),
    path('orders/', include('orders.urls')),


]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)