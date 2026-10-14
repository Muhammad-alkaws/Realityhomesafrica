from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'get_role', 'phone_number', 'is_active']
    list_filter = ['is_agent', 'is_tradesman', 'is_client', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('RealityHomesAfrica', {'fields': ('is_agent', 'is_tradesman', 'is_client', 'phone_number', 'profile_picture', 'bio')}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'subject', 'is_read', 'timestamp']
    list_filter = ['is_read']
