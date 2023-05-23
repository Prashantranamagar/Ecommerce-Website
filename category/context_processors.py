from .models import Category, SubCategory, SubSubCategory

from .models import Category

def category_links(request):
    subcategory = SubCategory.objects.all()
    subsubcategory = SubSubCategory.objects.all()
    category =  Category.objects.all()
	
    return dict(category=category, subcategory=subcategory, subsubcategory=subsubcategory)


    
