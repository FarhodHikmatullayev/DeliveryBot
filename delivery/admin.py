from django.contrib import admin
from .models import *


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'joined_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'time_limit', 'created_at')
