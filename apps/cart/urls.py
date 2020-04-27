# encoding: utf-8
"""
Author: Alvin
Contact: 673721260@qq.com
File: urls.py
Time: 2019/11/2 22:07
Desc:
"""

from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('add_cart/', views.CartView.as_view(), name='add_cart'),
    path('change_cart/', views.CartChangeView.as_view(), name='change_cart'),
    path('del_goods/', views.CartDelView.as_view(), name='del_goods')
]
