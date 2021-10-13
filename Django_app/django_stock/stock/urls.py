from django.urls import path
from . import views
urlpatterns = [
    path('stock/',views.finance_chart, name='Overview'), #our-domain.com/stock
    path('stock/chart',views.chart),
    path('stock/<Symbol>/finance_chart/', views.finance_chart, name='finance_chart'),
    # path('stock/<slug:Symbol>/finance-chart/', views.finance_chart, name='finance-chart')
]