# -*- coding: utf-8 -*-


#from django.contrib import admin
from django.urls import path
from main.views import MainPageView, UsersSiteView, LogginView, LkView, LkTaskView, RolesView#, RolesRosView
#app_name = 'index'

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('users', UsersSiteView.as_view(), name='users'),
    path('loggin/', LogginView.as_view(), name='loggin'),
    path('lk/', LkView.as_view(), name='lk'),
    path('lk_task/', LkTaskView.as_view(), name='lk_task'),
    path('roles/', RolesView.as_view(), name='roles'),
    #path('roless/', RolesRosView.as_view(), name='roless'),
]
