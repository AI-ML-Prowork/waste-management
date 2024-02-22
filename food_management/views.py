from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem, FoodCategory
from .forms import FoodItemForm,NewCategoryForm




def base(request):
    return render(request, 'base.html')



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
            return redirect('add_food_item')
    else:
        form = FoodItemForm()
    return render(request, 'food_management/add_food_item.html', {'form': form})


def food_item_list(request):
    food_items = FoodItem.objects.filter(added_by=request.user)
    return render(request, 'food_management/food_item_list.html', {'food_items': food_items})


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


def delete_food_item(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_item_list')
    return render(request, 'food_management/delete_food_item_confirm.html', {'food_item': food_item})





def add_category(request):
    if request.method == 'POST':
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_food_item')
    else:
        form = NewCategoryForm()
    return render(request, 'food_management/add_category.html', {'form': form})


def category_list(request):
    categories = FoodCategory.objects.all()
    return render(request, 'food_management/category_list.html', {'categories': categories})


def delete_category(request, pk):
     category = get_object_or_404(FoodCategory, pk=pk)
     if request.method == 'POST':
         category.delete()
         return redirect('add_food_item') 
     return render(request, 'food_management/delete_category_confirm.html', {'category': category})

