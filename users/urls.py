from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='user-dashboard'),
    path('post/', views.create_post, name='create-post'),
    path('fullpost/<post_id>', views.full_post, name='full-post'),
    path('rate/<post_id>/', views.add_ratings),
    path('posts/filtered/<query>/', views.results, name='results'),
    path('get/users/', views.get_users)
]