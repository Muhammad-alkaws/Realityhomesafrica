from django.contrib import admin
from .models import TradesmanProfile, PortfolioItem, ServiceRequest


@admin.register(TradesmanProfile)
class TradesmanProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'trade_category', 'location_city', 'is_verified', 'years_experience']
    list_filter = ['trade_category', 'is_verified']
    actions = ['verify_tradesmen']

    def verify_tradesmen(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected tradesmen have been verified.")
    verify_tradesmen.short_description = "Mark selected tradesmen as verified"


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'tradesman', 'completed_date']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'tradesman', 'trade_needed', 'status', 'created_at']
    list_filter = ['status']
