from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('posts/', views.getPosts),
    path('posts/<str:pk>/', views.getRoomCategories),
]