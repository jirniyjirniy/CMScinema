from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import RegisterAjaxView, LoginAjaxView, single_login

app_name = 'user'

urlpatterns = [
    # path('register/', register, name='register'),
    # path('register_success/', register_done, name='register_done'),
    path('register/', RegisterAjaxView.as_view(), name='register_ajax'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginAjaxView.as_view(), name='login_ajax'),
    path('single_login/', single_login, name='single_login')
]