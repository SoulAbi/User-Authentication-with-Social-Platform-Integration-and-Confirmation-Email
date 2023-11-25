# urls.py
from django.urls import path
from .views import register_user, verify_email, login_user


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('verify_email/<str:token>/', verify_email, name='verify-email'),
    path('login/', login_user, name='login_user'),

    
]
