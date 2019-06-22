# -*- coding: utf-8 -*-
# Author:李星宇
from django.urls import path
from . import views

app_name = 'userspace'
urlpatterns = [
    path('login', views.login, name='login'),
    path('loginhandle', views.loginhandle, name='loginhandle'),
    path('signin', views.sign_in, name='signin'),
    path('message', views.message, name='message'),
    path('collection', views.collection, name='collection'),
    path('histroy', views.histroy, name='histroy'),
    path('balance', views.balance, name='balance'),
    path('active', views.useractivityspace, name='useractivityspace'),
    path('userdetails', views.userdetails, name='userdetails'),
    path('', views.home, name='home'),


    path('clearsession', views.clearsession),
    path('clearrank', views.clear_book_rank),
    path('createuser', views.createuser),
]
