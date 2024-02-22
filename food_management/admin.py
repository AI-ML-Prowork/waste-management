from django.contrib import admin
from food_management.models import FoodCategory

class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(FoodCategory, FoodCategoryAdmin)


from food_management.models import FoodItem

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity','unit', 'expiry_date']

admin.site.register(FoodItem, FoodItemAdmin)

