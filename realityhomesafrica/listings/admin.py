from django.contrib import admin
from .models import Property, PropertyImage, Inspection, Favorite


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'agent', 'city', 'state', 'property_type', 'price', 'is_available', 'created_at']
    list_filter = ['property_type', 'state', 'is_available']
    search_fields = ['title', 'city', 'address']
    inlines = [PropertyImageInline]


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ['property', 'client', 'agent', 'requested_date', 'status']
    list_filter = ['status']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']
