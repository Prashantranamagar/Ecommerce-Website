from django.contrib import admin
from .models import Products, Variation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')    # to show image thumbnail in admin
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name', 'slug', 'price', 'is_available', 'category')
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active',)
    list_editable = ('is_active',)
    list_filter =('product', 'variation_categoty', 'variation_value')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Variation)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)

