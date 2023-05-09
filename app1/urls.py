from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name = 'index'),
    path('index', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),

    path('postpage/<str:pk>', views.postpage, name = 'postpage'),
    path('posts/<int:pk>/preference/<int:userpreference>/', views.postpreference, name='postpreference'),

    #path('post/<str:pk>/<str:userpreference>', views.postpreference, name='postpreference'),
    # path('likePst/<str:pk>', views.like_post, name = 'like_post'),
    # path('dislikePost/<str:pk>', views.dislike_post, name = 'dislike_post'),
    # path('heartPost/<str:pk>', views.heart_post, name = 'heart_post'),


    path('create_post', views.create_post, name = 'create_post'),
    path('updatePost/<str:pk>', views.updatePost, name = 'updatePost'),
    path('deletePost/<str:pk>', views.deletePost, name = 'deletePost'),
    path('category/<str:pk>', views.category, name = 'category'),
    
    path('logout', views.logout, name = 'logout'),
    path('about', views.about, name = 'about'),
    path('contact', views.contact, name = 'contact'),
    path('page', views.page, name = 'page'),

    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:uid>/<str:token>/', views.reset_password, name='reset_password'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

