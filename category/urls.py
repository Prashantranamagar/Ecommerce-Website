from django.urls import path
from . import views

urlpatterns = [
    path('<slug:cat_slug>', views.category, name='category'),
    path('<slug:cslug>/<slug:sslug>', views.subcategory, name='subcat'),
    path('<slug:cslug>/<slug:sslug>/<slug:ssslug>', views.subsubcategory, name='subsubcat'),
    
]