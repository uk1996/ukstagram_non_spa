from django.contrib.auth.validators import UnicodeUsernameValidator
from django.urls import path, register_converter
from . import views
from .converters import UsernameConverter

app_name = 'ukstagram'

register_converter(UsernameConverter, 'username')

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
   # path('<username:username>/', views.user_page, name='user_page'),
    path('<str:username>/', views.user_page, name='user_page'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/unlike/', views.post_unlike, name='post_unlike'),
]