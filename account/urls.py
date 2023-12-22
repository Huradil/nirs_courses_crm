from django.urls import path
from django.contrib.auth.views import LogoutView
from global_login_required import login_not_required

from . import views

urlpatterns = [
  path('register/', login_not_required(views.UserCreateView.as_view()), name='register'),
  path('login/', login_not_required(views.UserLoginView.as_view()), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]
