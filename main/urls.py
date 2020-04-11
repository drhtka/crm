# -*- coding: utf-8 -*-


#from django.contrib import admin
from django.urls import path
from main.views import MainPageView, UsersSiteView
app_name = 'index'

urlpatterns = [
    path('main/', MainPageView.as_view(), name='main'),
    path('users', UsersSiteView.as_view(), name='users'),

]
