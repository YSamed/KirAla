from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myadmin'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.myadmin_login, name='myadmin_login'),
    path('logout/', views.myadmin_logout, name='myadmin_logout'),
    path('register/', views.myadmin_register, name='myadmin_register'),
    path('tenant-list/', views.tenant_list, name='tenant_list'),

]
