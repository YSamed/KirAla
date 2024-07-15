from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
from .models import Contract, Apartment ,Building
from .forms import ContractForm 

class ContractListView(ListView):
    model = Contract
    template_name = 'contract/contract_list.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        return Contract.objects.filter(is_active=True,is_deleted=False)  

class ContractDetailView(DetailView):
    model = Contract
    template_name = 'contract/contract_detail.html'
    context_object_name = 'contract'

    def post(self, request, *args, **kwargs):
        if 'soft_delete' in request.POST:
            contract = self.get_object()
            contract.is_deleted = True  # veya False, isteğinize bağlı olarak
            contract.save()
            messages.success(request, 'Contract has been deleted successfully.')
            return redirect('contract:contract-list')  # Silinen sözleşmelerin listesi
        return super().post(request, *args, **kwargs)

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contract/contract_create.html'
    success_url = reverse_lazy('contract:contract-list')

    def form_valid(self, form):
        # Check if there is already a contract for this apartment and tenant
        apartment = form.cleaned_data['apartment']
        tenant = form.cleaned_data['tenant']
        
        existing_contract = Contract.objects.filter(apartment=apartment, tenant=tenant).exists()
        if existing_contract:
            messages.error(self.request, 'A contract already exists for this apartment and tenant.')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Contract has been created successfully.')
        return super().form_valid(form)

class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contract/contract_update.html'
    success_url = reverse_lazy('contract:contract-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        contract = self.get_object()
        kwargs['initial'] = {'apartment': contract.apartment} 
        return kwargs

    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.save()

        messages.success(self.request, 'Contract has been updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('properties:building-detail', kwargs={'pk': self.object.apartment.building.pk})

class ContractHistoryView(ListView):
    model = Contract
    template_name = 'contract/contract_history.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        return Contract.objects.filter(is_active=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.today().date()
        return context