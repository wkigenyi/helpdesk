from django.urls import path
from django.contrib.auth import views
from . import views as my_views
urlpatterns = [
    path('login/',views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('profile/',my_views.my_tickets,name='profile'),
    path('password_reset',views.PasswordResetView.as_view(template_name='users/reset_password.html'),name='password_reset'),
    path('register',my_views.register,name='register')
]