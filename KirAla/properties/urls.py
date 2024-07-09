from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/step1/', views.property_create_step1, name='property_create_step1'),
    path('property/create/step2/', views.property_create_step2, name='property_create_step2'),
    path('<int:pk>/update/step1/', views.property_update_step1, name='property_update_step1'),
    path('<int:pk>/update/step2/', views.property_update_step2, name='property_update_step2'),
    path('<int:pk>/delete/', views.property_delete, name='property_delete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
