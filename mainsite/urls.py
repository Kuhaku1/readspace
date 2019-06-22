# -*- coding: utf-8 -*-
# Author:李星宇
from django.urls import path
from . import views
from userspace import views as loginview

app_name = 'mainsite'
urlpatterns = [
    path('ck/', views.cke),
    path('login', loginview.login, name='login'),
    path('', views.index, name="index"),
    path('book_<int:bookid>', views.get_book_info, name='book'),
    path('book/sid_<int:sid>', views.get_book_context, name='read'),
    # path('book', views.get_book_info, name='book'),
    path('screen', views.sceen, name='screen'),
    path('search', views.search, name='search'),
    path('novelrank', views.novelrank, name='novelrank'),
    path('novelrank_<int:year>', views.novelrankyear, name='novelrankyear'),
    path('init', views.clear, name='clear'),
]
