from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import BuildingListView, BuildingDetailView, BuildingCreateView, BuildingUpdateView 

app_name = 'properties'

urlpatterns = [
    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('building/<int:pk>/', BuildingDetailView.as_view(), name='building-detail'),
    path('building/create/', BuildingCreateView.as_view(), name='building-create'),
    path('building/<int:pk>/update/', BuildingUpdateView.as_view(), name='building-update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
