from django.urls import path, include
from . import api_views

urlpatterns = [
    # category
    path('categories/', api_views.category_list),
    path('categories/search/', api_views.category_search),
    path('categories/create/', api_views.category_create),
    path('categories/update/<int:pk>/', api_views.category_update_delete),
    path('categories/delete/<int:pk>/', api_views.category_update_delete),

    path('categories/<int:pk>/topics/', api_views.categories_topics),


    # topic
    path('topics/', api_views.topic_list),
    path('topics/search/', api_views.topic_search),
    path('topics/create/', api_views.topic_create),
    path('topics/update/<int:pk>/', api_views.topic_update_delete),
    path('topics/delete/<int:pk>/', api_views.topic_update_delete),

    # post
    path('posts/', api_views.post_list),
    path('posts/create/', api_views.post_create),
    path('posts/update/<int:pk>/', api_views.post_update),
    path('posts/delete/<int:pk>/', api_views.post_delete),

    path('users/posts/', api_views.user_posts),
]