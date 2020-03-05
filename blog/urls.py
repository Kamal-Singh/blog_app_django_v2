from django.urls import path
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('signup', views.user_signup, name='user_signup'),
    path("signin", views.user_signin, name='user_signin'),
    path('logout', views.user_logout, name='user_logout'),
    path('createblog', views.create_blog, name='create_blog'),
    path('editblog/<int:blog_id>/', views.edit_blog, name = 'edit_blog'),    
]