from django.contrib import admin
from django.urls import path
from snippet_app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index_page/',index_page,name='index_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('dashboard/',dashboard,name='dashboard'),
    path('register/', register_user, name='register'),
    path('add_snippet/', add_snippet, name='add_snippet'),
    path('create_snippet/', create_snippet, name='create_snippet'),
    path('do_logout/', do_logout, name='do_logout'),
    path('list_all_snippets/', list_all_snippets, name='list_all_snippets'),
    path('get_all_snippets/', get_all_snippets, name='get_all_snippets'),
    path('detail/<int:pk>/', snippet_detail, name='snippet_detail'),
    path('edit_snippet_page/', edit_snippet_page, name='edit_snippet_page'),
    path('update_snippet/<int:pk>/', update_snippet, name='update_snippet'),
    path('delete_snippets/', delete_snippets, name='delete_snippets'),
    path('list_all_tags/', list_all_tags, name='list_all_tags'),
    path('get_all_tags/', get_all_tags, name='get_all_tags'),
    path('get_content_by_tag/<str:tag_title>/', get_content_by_tag, name='get_content_by_tag'),
    # path('handler404page/', handler404page, name='handler404page'),
 
]



