from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
from .models import Contract, Apartment
from .forms import ContractForm 


class ContractListView(ListView):
    model = Contract
    template_name = 'contract/contract_list.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        landlord = self.request.user.landlord 

        return Contract.objects.filter(landlord=landlord, is_active=True, is_deleted=False)

class ContractDetailView(DetailView):
    model = Contract
    template_name = 'contract/contract_detail.html'
    context_object_name = 'contract'

    def post(self, request, *args, **kwargs):
        if 'soft_delete' in request.POST:
            contract = self.get_object()
            contract.is_deleted = True
            contract.save()
            messages.success(request, 'Contract has been deleted successfully.')
            return redirect('contract:contract-list') 
        return super().post(request, *args, **kwargs)

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contract/contract_create.html'
    success_url = reverse_lazy('contract:contract-list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user.landlord
        form.fields['apartment'].queryset = Apartment.objects.filter(landlord=self.request.user.landlord)
        end_date = form.cleaned_data['end_date']
        if end_date < datetime.today().date():
            form.instance.is_active = False
        else:
            form.instance.is_active = True
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
        today = datetime.today().date()
        return Contract.objects.filter(end_date__lt=today, is_deleted=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.today().date()
        return context