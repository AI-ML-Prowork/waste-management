from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    pre_expiry_days = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name

class FoodItem(models.Model):
    UNIT_CHOICES = [
        ('kg', 'kg'),
        ('g', 'g'),
        ('ml', 'ml'),
        ('pieces', 'pieces'),
        ('packets', 'packets'),
        ('litres', 'litres'),
        ('units', 'units'),
        ('other', 'other'),
    ]    
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    expiry_date = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    def calculate_expiry_date(self):
        pre_expiry_days = self.category.pre_expiry_days
        return self.expiry_date - timezone.timedelta(days=pre_expiry_days)

    def calculate_expiry_date(self):
        pre_expiry_days = self.category.pre_expiry_days
        return self.expiry_date - timezone.timedelta(days=pre_expiry_days)
    
    def __str__(self):
        return self.name


class FoodBank(models.Model):
    Food_bank_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class BarcodeFoodItem(models.Model):
    name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    barcode_image = models.ImageField(upload_to='barcode_images/')

    def __str__(self):
        return self.name