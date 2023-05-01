from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('index', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('postpage/<str:pk>', views.postpage, name = 'postpage'),
    path('create_post', views.create_post, name = 'create_post'),
    path('updatePost/<str:pk>', views.updatePost, name = 'updatePost'),
    path('category/<str:pk>', views.category, name = 'categorypage'),
    
    path('logout', views.logout, name = 'logout'),
    path('about', views.about, name = 'about'),
    path('contact', views.contact, name = 'contact'),
    path('page', views.page, name = 'page'),

    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),


]
