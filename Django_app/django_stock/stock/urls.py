from django.urls import path
from . import views   #ชื่อฟังชั่นที่สร้างไว้ใน views.py
urlpatterns = [
    path('stock/',views.symbol_company, name='Overview'), #our-domain.com/stock
    path('stock/chart',views.chart),
    path('stock/<Symbol>/finance_chart/', views.finance_chart, name='finance_chart'),
    # path('stock/<slug:Symbol>/finance-chart/', views.finance_chart, name='finance-chart')
]
