# encoding: utf-8
"""
Author: Alvin
Contact: 673721260@qq.com
File: urls.py
Time: 2019/11/2 22:07
Desc:
"""

from django.urls import path
from goods import views

app_name = 'goods'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('details/<int:goods_id>', views.DetailsView.as_view(), name='details'),
    path('list/<int:type_id>', views.ListView.as_view(), name='list')
]
