# encoding: utf-8
"""
Author: Alvin
Contact: 673721260@qq.com
File: urls.py
Time: 2019/11/2 22:07
Desc:
"""

from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('active/<token>', views.ActiveView.as_view(), name='active'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('userinfo/', views.UserCenterView.as_view(), name='userinfo'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('address/', views.AddressView.as_view(), name='address')
]
