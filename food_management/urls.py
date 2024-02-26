from django.urls import path
from . views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('base', base, name='base'),
    
    path('add_category/', add_category, name='add_category'),
    path('category_list/', category_list, name='category_list'),
    path('delete_category/<int:pk>/', delete_category, name='delete_category'),

    path('add_food_item/', add_food_item, name='add_food_item'),
    path('food_item_list/', food_item_list, name='food_item_list'),
    path('edit_food_item/<int:pk>/', edit_food_item, name='edit_food_item'),
    path('delete_food_item/<int:pk>/', delete_food_item, name='delete_food_item'),

    path('add_food_bank/', add_food_bank, name='add_food_bank'),
    path('food_bank_list/', food_bank_list, name='food_bank_list'),

    path('user_login/', user_login, name='user_login'),
    path('user_signup/', user_signup, name='user_signup'),
    path('user_logout/', user_logout, name="user_logout"),



]
