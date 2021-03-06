from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('resources/', all_resources, name='all-resources'),
    path('new/resource/', post_resource, name='post_resource'),
    path('like/<int:pk>/', like_resource, name='like_resource'),
    path('dislike/<int:pk>/', dislike_resource, name='like_resource'),
]
