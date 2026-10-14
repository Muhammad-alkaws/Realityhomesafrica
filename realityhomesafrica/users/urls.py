from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
    path('register/client/', views.register_client, name='register_client'),
    path('register/agent/', views.register_agent, name='register_agent'),
    path('register/tradesman/', views.register_tradesman, name='register_tradesman'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:pk>/', views.message_detail, name='message_detail'),
    path('message/<int:receiver_id>/', views.send_message, name='send_message'),
]
