# encoding: utf-8
"""
Author: Alvin
Contact: 673721260@qq.com
File: urls.py
Time: 2019/11/2 22:07
Desc:
"""

from django.urls import path
from order import views

app_name = 'orders'
urlpatterns = [
    path('', views.OrderView.as_view(), name='orders'),
    path('commit/', views.OrderCommitView.as_view(), name='commit'),
    path('myorders/', views.MyOrdersView.as_view(), name='myorders'),
    path('payorder/', views.OrderPayView.as_view(), name='payorder'),
    path('orderquery/', views.OrderStatusQueryView.as_view(), name='query')
]
