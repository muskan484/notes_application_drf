from django.urls import path
from .views import UserSignUp, UserLogin

urlpatterns = [
    path('signup',UserSignUp.as_view(), name='user-signup'),
    path('login',UserLogin.as_view(), name='user-login')
]