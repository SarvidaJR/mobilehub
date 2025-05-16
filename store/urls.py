# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('phones/', views.phone_list, name='phone_list'),
    path('phones/<int:phone_id>/', views.phone_detail, name='phone_detail'),
    path('add-phone/', views.add_phone, name='add_phone'),
    path('phones/<int:phone_id>/edit/', views.edit_phone, name='edit_phone'),
    path('phones/<int:phone_id>/delete/', views.delete_phone, name='delete_phone'),
    path('buy/', views.buy_phone, name='buy_phone'),
    path('orders/', views.customer_orders, name='customer_orders'), 
    path('phones/update-stock/<int:phone_id>/', views.update_stock, name='update_stock'),
    path('orders/filter/', views.filter_orders_by_payment, name='filter_orders_by_payment'),
    path('customers/<int:customer_id>/', views.customer_profile, name='customer_profile'),
    path('dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path('upc-lookup/', views.upc_lookup, name='upc_lookup'),
    
]
