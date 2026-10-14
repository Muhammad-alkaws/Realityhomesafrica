from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.tradesman_list, name='tradesman_list'),
    path('tradesman/<int:pk>/', views.tradesman_profile, name='tradesman_profile'),
    path('dashboard/', views.tradesman_dashboard, name='tradesman_dashboard'),
    path('dashboard/portfolio/add/', views.add_portfolio_item, name='add_portfolio_item'),
    path('request/<int:tradesman_pk>/', views.request_service, name='request_service'),
    path('my-requests/', views.tradesman_requests, name='tradesman_requests'),
]
