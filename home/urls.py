from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('blog/favorite/<int:blog_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('blog/', views.blog, name='blog'),
    path('projects/', views.projects, name='projects'),
    path('login_user/', views.login_user, name='login_user'),
    path('LogoutUser/', views.LogoutUser, name='LogoutUser'),
    path('register/', views.register_user, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('activation-countdown/', views.activation_countdown, name='activation_countdown'),
    path('blogpost/<int:id>/', views.blogpost, name='blogpost'),
    path('search/', views.search, name='search'),
    path('thanks/', views.thanks, name='thanks'),
    path('project_detail/<int:id>/', views.project_detail, name='project_detail'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('add_project/', views.add_project, name='add_project'),
]
