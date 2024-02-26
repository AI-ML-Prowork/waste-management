from django import forms
from .models import FoodItem, FoodCategory,FoodBank

class FoodItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FoodItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = FoodCategory.objects.all()


    

    class Meta:
        model = FoodItem
        fields = ['category', 'name', 'quantity','unit','expiry_date', 'barcode']
        widgets= {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


class NewCategoryForm(forms.ModelForm):
    pre_expiry_days = forms.IntegerField(label='Pre-Expiry Days', initial=0) 

    class Meta:
        model = FoodCategory
        fields = ['name', 'pre_expiry_days']


class FoodBankForm(forms.ModelForm):

    
    class Meta:
        model = FoodBank
        fields = ['Food_bank_name', 'location']

