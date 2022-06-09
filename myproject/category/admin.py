from django.contrib import admin
from .models import Category, SubCategory, SubSubCategory

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('cat_name',)} #to auto generate slug with cat_name
	list_display = ('cat_name', 'slug')

admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('subcat_name',)} #to auto generate slug with subcat_name
	list_display = ('subcat_name', 'slug', 'cat_name')


admin.site.register(SubCategory, SubCategoryAdmin)


class SubSubCategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('subsubcat_name',)} #to auto generate slug with subsubcat_name
	list_display = ('subsubcat_name', 'slug', 'subcat_name')


admin.site.register(SubSubCategory, SubSubCategoryAdmin)
