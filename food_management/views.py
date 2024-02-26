from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem, FoodCategory
from .forms import FoodItemForm,NewCategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import os,io,base64,barcode
from barcode.writer import ImageWriter
from django.utils import timezone
from io import BytesIO


@login_required(login_url='user_login/')
def dashboard(request):
    total_users = User.objects.count()
    total_food_items = FoodItem.objects.count()
    total_categories = FoodCategory.objects.count()

    approaching_expiry_items = []
    for category in FoodCategory.objects.all():
        pre_expiry_days = category.pre_expiry_days
        approaching_expiry_items.extend(
            FoodItem.objects.filter(
                category=category,
                expiry_date__lte=timezone.now() + timezone.timedelta(days=pre_expiry_days)
            )
        )

    return render(request, 'food_management/dashboard.html', {
        'total_users': total_users,
        'total_food_items': total_food_items,
        'total_categories': total_categories,
        'approaching_expiry_items': approaching_expiry_items
    })


@login_required(login_url='user_login/')
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            new_category = form.cleaned_data.get('new_category')

            if not category and new_category:
                category = FoodCategory.objects.create(name=new_category)            
            food_item = form.save(commit=False)
            food_item.added_by = request.user
            food_item.category = category
            food_item.save()
            barcode_data = f"{food_item.name} {food_item.category} {food_item.expiry_date}"
            barcode_image = generate_barcode_image(barcode_data)
            return render(request, 'food_management/add_food_item.html', {'form': form, 'barcode_image': barcode_image})                   
    else:
        form = FoodItemForm()
    return render(request, 'food_management/add_food_item.html', {'form': form})

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.base import ContentFile

def generate_barcode_image(barcode_data):
    code128 = barcode.get_barcode_class('code128')
    code = code128(barcode_data, writer=ImageWriter())
    buffer = io.BytesIO()
    code.write(buffer)
    image_data = buffer.getvalue()
    base64_image = base64.b64encode(image_data)
    return base64_image.decode('utf-8')

@login_required(login_url='user_login/')
def food_item_list(request):
    food_items = FoodItem.objects.filter(added_by=request.user)
    return render(request, 'food_management/food_item_list.html', {'food_items': food_items})



@login_required(login_url='user_login/')
def edit_food_item(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('food_item_list')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'food_management/edit_food_item.html', {'form': form})



@login_required(login_url='user_login/')
def delete_food_item(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_item_list')
    return render(request, 'food_management/delete_food_item_confirm.html', {'food_item': food_item})


@login_required(login_url='user_login/')
def add_category(request):
    if request.method == 'POST':
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_food_item')
    else:
        form = NewCategoryForm()
    return render(request, 'food_management/add_category.html', {'form': form})




@login_required(login_url='user_login/')
def category_list(request):
    categories = FoodCategory.objects.all()
    pre_expiry_days = FoodCategory.objects.all()
    return render(request, 'food_management/category_list.html', {'categories': categories, 'pre_expiry_days': pre_expiry_days})





@login_required(login_url='user_login/')
def delete_category(request, pk):
     category = get_object_or_404(FoodCategory, pk=pk)
     if request.method == 'POST':
         category.delete()
         return redirect('add_food_item') 
     return render(request, 'food_management/delete_category_confirm.html', {'category': category})


from .forms import FoodBankForm
from .models import FoodBank

@login_required(login_url='user_login/')
def add_food_bank(request):
    if request.method == 'POST':
        form = FoodBankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_food_bank')
    else:
        form = FoodBankForm()
    return render(request, 'food_management/add_food_bank.html', {'form': form})


def food_bank_list(request):
    Food_bank_name = FoodBank.objects.all()
    location = FoodBank.objects.all()

    return render(request, 'food_management/food_bank_list.html', {'Food_bank_name': Food_bank_name, 'location': location})




def user_signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        first_name = request.POST.get('First_Name')
        last_name = request.POST.get('Last_Name')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        confirm_password = request.POST.get('Confirm_Password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('user_signup')
        

        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )


        messages.success(request, 'Account created successfully')
        return redirect('user_login') 
    
    return render(request, 'auth/user_signup.html')



def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None and not user.is_superuser:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'auth/user_login.html')

@login_required(login_url='user_login/')
def user_logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('user_login')


@login_required(login_url='user_login/')
def base(request):
    return render(request, 'base.html')

