# -*- coding: utf-8 -*-
# Author:李星宇
from django.urls import path
from . import views
from userspace import views as loginview

app_name = 'api'
urlpatterns = [
    path('signinhandle', views.sign_in_handle, name="signinhandle"),
    path('screenbook', views.find_book_from_screen, name="findbook"),
    path('searchbook', views.search_book_from_search_view, name="searchbook"),
    path('booklike', views.booklike_view, name="booklike"),
    path('bookcollection', views.bookcollection_view, name="bookcollection"),
    path('bookcoin', views.bookcoin_view, name="bookcoin"),
    path('readtimehandle', views.readtimehandle, name="readtimehandle"),
    path('comment', views.view_user_submit_comment, name="usercomment"),
]
