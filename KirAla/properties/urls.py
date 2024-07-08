# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('create/', views.property_create, name='property_create'),
    path('create/step2/', views.property_create_step2, name='property_create_step2'),
    path('<int:pk>/update/step1/', views.property_update_step1, name='property_update_step1'),
    path('<int:pk>/update/step2/', views.property_update_step2, name='property_update_step2'),
    path('<int:pk>/delete/', views.property_delete, name='property_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
