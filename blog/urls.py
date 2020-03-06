from django.urls import path
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('signup', views.user_signup, name='user_signup'),
    path("signin", views.user_signin, name='user_signin'),
    path('logout', views.user_logout, name='user_logout'),
    path('createblog', views.create_blog, name='create_blog'),
    path('editblog/<uuid:blog_id>/', views.edit_blog, name = 'edit_blog'),    
    path('blog/<uuid:blog_id>/', views.view_blog, name = 'view_blog'),
    path('', views.index, name = 'index'),
    path('delete/<uuid:blog_id>/', views.delete_blog, name = 'delete_blog'),
]