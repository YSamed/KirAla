from django.urls import path ,include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:order_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:order_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

  



    
]
