from django.urls import path
from . import views
urlpatterns = [
    path('stock/',views.symbol_company, name='Overview'), #our-domain.com/stock
    path('stock/<Symbol>/', views.stockholder, name='stock'),
    path('stock/<Symbol>/', views.stock_info,name='stock')
]