from django.contrib import admin

from user.models import UserProfile, UserOrder, Address, City, Region
from .models import User


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user_type')
    search_fields = ('email',)


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'phone', 'address')
    search_fields = ('user',)


@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'total_price')
    search_fields = ('user',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'city', 'map_link')
    search_fields = ('city',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'name', 'map_link')
    search_fields = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'map_link')
    search_fields = ('name',)
