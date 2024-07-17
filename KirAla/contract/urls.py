from django.urls import path 
from .views import ContractListView, ContractDetailView ,ContractCreateView ,ContractUpdateView ,ContractHistoryView

app_name = 'contract'

urlpatterns = [
    path('', ContractListView.as_view(), name='contract-list'),
    path('<int:pk>/', ContractDetailView.as_view(), name='contract-detail'),
    path('create/', ContractCreateView.as_view(), name='contract-create'),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name='contract-update'),
    path('history/', ContractHistoryView.as_view(), name='contract-history'),

]