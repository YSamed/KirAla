from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import BuildingListView, BuildingDetailView, BuildingCreateView, BuildingUpdateView, ApartmentListView, ApartmentCreateView, ApartmentDetailView, ApartmentUpdateView

app_name = 'properties'

urlpatterns = [

    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('building/<int:pk>/', BuildingDetailView.as_view(), name='building-detail'),
    path('building/create/', BuildingCreateView.as_view(), name='building-create'),
    path('building/<int:pk>/update/', BuildingUpdateView.as_view(), name='building-update'),

    path('apartments/', ApartmentListView.as_view(), name='apartment-list'),
    path('building/<int:pk>/apartment-create/', ApartmentCreateView.as_view(), name='apartment-create'),
    path('apartment/<int:pk>/', ApartmentDetailView.as_view(), name='apartment-detail'),
    path('apartments/<int:pk>/update/', ApartmentUpdateView.as_view(), name='apartment-update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
