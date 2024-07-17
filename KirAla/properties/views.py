from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Building, Apartment , Landlord
from .forms import BuildingForm, ApartmentForm


class BuildingListView(ListView):
    model = Building
    template_name = 'building_list.html'
    context_object_name = 'buildings'

    def get_queryset(self):
        return Building.objects.filter(landlord__user=self.request.user, is_deleted=False)

class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'properties/building_create.html'
    success_url = reverse_lazy('properties:building-list')

    def form_valid(self, form):
        landlord = Landlord.objects.get(user=self.request.user)
        building = form.save(commit=False)
        building.landlord = landlord
        building.save()
        messages.success(self.request, 'Building has been created successfully.')
        return super().form_valid(form)

class BuildingDetailView(DetailView):
    model = Building
    template_name = 'properties/building_detail.html'
    context_object_name = 'building'

    def post(self, request, *args, **kwargs):
        building = self.get_object()
        
        if 'delete_apartment' in request.POST:
            apartment_pk = request.POST.get('delete_apartment')
            apartment = get_object_or_404(Apartment, pk=apartment_pk)
            apartment.is_deleted = True
            apartment.save()
            messages.success(request, 'Apartment has been marked as deleted.')
            return redirect('properties:building-detail', pk=building.pk)

        return redirect('properties:building-detail', pk=building.pk)

class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'properties/building_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Building has been updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('properties:building-detail', kwargs={'pk': self.object.pk})


class ApartmentListView(ListView):
    model = Apartment
    template_name = 'properties/apartment_list.html'
    context_object_name = 'apartments'

    def get_queryset(self):
        return Apartment.objects.filter(is_deleted=False)

class ApartmentCreateView(CreateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'properties/apartment_create.html'
    success_url = reverse_lazy('properties:building-list')

    def form_valid(self, form):
        building_id = self.kwargs.get('pk')
        building = get_object_or_404(Building, pk=building_id)
        apartment = form.save(commit=False)
        apartment.building = building
        apartment.save()
        
        building.rental_apartment_count += 1
        building.save()

        self.success_url = reverse_lazy('properties:building-detail', kwargs={'pk': building.pk})
        messages.success(self.request, 'Apartment has been created successfully.')
        return super().form_valid(form)

class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = 'properties/apartment_detail.html'
    context_object_name = 'apartment'

    def post(self, request, *args, **kwargs):
        if 'delete_apartment' in request.POST:
            apartment = self.get_object()
            apartment.is_deleted = True
            apartment.save()
            messages.success(request, 'Apartment has been deleted successfully.')
            return redirect('properties:building-detail', pk=apartment.building.pk)

        return redirect('properties:apartment-detail', pk=self.get_object().pk)

class ApartmentUpdateView(UpdateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'properties/apartment_update.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        new_is_rented = form.cleaned_data['is_rented']
        old_is_rented = instance.is_rented

        if old_is_rented != new_is_rented:
            if new_is_rented:
                instance.building.rental_apartment_count += 1
            else:
                instance.building.rental_apartment_count -= 1
            instance.building.save()

        messages.success(self.request, 'Apartment has been updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('properties:apartment-detail', kwargs={'pk': self.object.pk})
