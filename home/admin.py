from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['category','subcategory','product_name','price','discount_price','image',]
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=['title','subtitle','image','content','timestamp','author',]
@admin.register(orderitem)
class orderitemAdmin(admin.ModelAdmin):
    list_display=['customer','product','price','name','address','phone','email','date',]
admin.site.register(About)
