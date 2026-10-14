from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('browse/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/', views.property_create, name='property_create'),
    path('property/<int:pk>/update/', views.property_update, name='property_update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('dashboard/inspections/', views.agent_inspections, name='agent_inspections'),
    path('property/<int:pk>/inspect/', views.request_inspection, name='request_inspection'),
    path('inspection/<int:pk>/confirm/', views.confirm_inspection, name='confirm_inspection'),
    path('inspection/<int:pk>/cancel/', views.cancel_inspection, name='cancel_inspection'),
    path('my-inspections/', views.client_inspections, name='client_inspections'),
    path('property/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]
