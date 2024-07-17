from django.urls import path ,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myadmin'

urlpatterns = [
    path('properties/', include('properties.urls')),
    path('index/', views.index, name='index'),
    path('', views.myadmin_login, name='myadmin_login'),
    path('logout/', views.myadmin_logout, name='myadmin_logout'),
    path('register/', views.myadmin_register, name='myadmin_register'),
    path('update/', views.myadmin_update, name='myadmin_update'),
    path('password_change/', views.myadmin_password_change, name='myadmin_password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='myadmin/password_change_done.html'), name='password_change_done'),
    path('tenant-list/', views.tenant_list, name='tenant_list'),
    path('landlord-list/', views.landlord_list, name='landlord_list'),

]
