from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path("password_change/", views.password_change, name="password_change"),
    path('<str:username>/follow/', views.user_follow, name='user_follow'),
    path('<str:username>/unfollow/', views.user_unfollow, name='user_unfollow'),
]