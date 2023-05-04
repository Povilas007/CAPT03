from django.urls import path,include
from . import views

# your URL patterns here

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('create-post/', views.create_post, name='tweet'),
    path('user-profile/', views.view_profile, name='user_profile'),
    path('users/profile/<int:user_id>/', views.profile, name='profile'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/update/', views.profile_update, name='profile_update'),
]
