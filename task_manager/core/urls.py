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
    path('<int:pk>/detail', views.detail, name='detail'),
    path('<int:pk>/delete', views.delete_task, name='delete_task'),
    path('<int:pk>/editTask', views.edit_task, name='edit_task'),
    path('<int:pk>/change_status', views.completed, name='completed_status'),
    path('<int:pk>/assign_user', views.assign_user, name='assign_user')
]