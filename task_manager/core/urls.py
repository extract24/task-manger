from django.urls import path
from . import views
from .forms import LogInForm
from django.contrib.auth import views as auth_view

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_view.LoginView.as_view(template_name='core/login.html', authentication_form=LogInForm), name='signin'),
    path('logout/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]