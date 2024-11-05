from django.contrib import admin
from .models import *

# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('food_names','description')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('category','name','price')


admin.site.register(Category)
admin.site.register(Items, ItemAdmin)
admin.site.register(Cart)
admin.site.register(Favourite)