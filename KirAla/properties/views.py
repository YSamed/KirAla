from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Building
from .forms import BuildingForm
from django.shortcuts import redirect

class BuildingListView(ListView):
    model = Building
    template_name = 'building_list.html'
    context_object_name = 'buildings' 

    def get_queryset(self):
        return Building.objects.filter(is_deleted=False)

class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'properties/building_create.html'  
    success_url = reverse_lazy('properties:building-list') 

    def form_valid(self, form):
        messages.success(self.request, 'Building has been created successfully.')  
        return super().form_valid(form)

class BuildingDetailView(DetailView):
    model = Building
    template_name = 'properties/building_detail.html' 
    context_object_name = 'building'  

    def get_queryset(self):
        return Building.objects.filter(is_deleted=False)
    
    def post(self, request, *args, **kwargs):
        if 'delete_building' in request.POST:
            building = self.get_object()
            building.is_deleted = True
            building.save()
            messages.success(request, 'Building has been deleted successfully.')
            return redirect('properties:building-list')
        return super().post(request, *args, **kwargs)
    
class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'properties/building_update.html'  # Güncelleme şablonu dosyası
    
    def get_success_url(self):
        return reverse_lazy('properties:building-detail', kwargs={'pk': self.object.pk})
