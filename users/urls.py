from django.urls import path,re_path,include
from django.contrib.auth import views
from . import views as my_views
urlpatterns = [
    
    path('login/',views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('profile/',my_views.my_tickets,name='profile'),
    path('password_reset',views.PasswordResetView.as_view(
        template_name='users/reset_password.html',
        html_email_template_name='users/password_reset_email.html',
        email_template_name='users/email.html',
        subject_template_name='users/subject.txt'
        ),name='password_reset'),
    path('register',my_views.register,name='register'),
    path('users',my_views.users,name='users'),
    path('profile/<int:id>/',my_views.user_profile,name='user_profile'),
    
    
]