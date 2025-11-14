from django.urls import path, include
from . import api_views

urlpatterns = [
    # category
    path('categories/', api_views.category_list),
    path('categories/search/', api_views.category_search),
    path('categories/create/', api_views.category_create),
    path('categories/<int:pk>/', api_views.category_detail),


    # topic
    path('topics/', api_views.topic_list),
    path('topics/search/', api_views.topic_search),
    path('topics/create/', api_views.topic_create),
    path('topics/<int:pk>/', api_views.topic_detail),

    # post
    path('posts/', api_views.post_list),
    path('posts/create/', api_views.post_create),
    path('posts/<int:pk>/', api_views.post_detail),
]