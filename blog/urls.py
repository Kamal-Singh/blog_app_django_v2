from django.urls import path
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('signup', views.user_signup, name='user signup'),
    path("signin", views.user_signin, name='user signin'),
    path('logout', views.user_logout, name='user logout'),
]