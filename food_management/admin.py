from django.contrib import admin
from food_management.models import FoodCategory

class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pre_expiry_days']

admin.site.register(FoodCategory, FoodCategoryAdmin)


from food_management.models import FoodItem

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity','unit', 'expiry_date']

admin.site.register(FoodItem, FoodItemAdmin)

from food_management.models import FoodBank

class FoodBankAdmin(admin.ModelAdmin):
    list_display = ['Food_bank_name', 'location']

admin.site.register(FoodBank, FoodBankAdmin)


from food_management.models import BarcodeFoodItem

class BarcodeFoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'expiry_date']

admin.site.register(BarcodeFoodItem, BarcodeFoodItemAdmin)