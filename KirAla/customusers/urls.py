from django.urls import path
from .views import CreateUserView, LandlordCreateView, TenantCreateView, AdminCreateView

app_name = 'customusers'

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('create-user/landlord/', LandlordCreateView.as_view(), name='create-landlord'),
    path('create-user/tenant/', TenantCreateView.as_view(), name='create-tenant'),
    path('create-user/admin/', AdminCreateView.as_view(), name='create-admin'),
]
