from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import LandlordForm, TenantForm
from .models import Landlord
from django.core.exceptions import PermissionDenied


class LandlordCreateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = LandlordForm()
            return render(request, 'customusers/landlord_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a landlord.')
            return redirect('myadmin:index')
    
    def post(self, request):
        if request.user.is_authenticated:
            form = LandlordForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Landlord user created successfully.')
                return redirect('tenant-list')  
            else:
                messages.error(request, 'Failed to create landlord. Please check the form.')
                return render(request, 'customusers/landlord_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a landlord.')
            return redirect('myadmin:index')
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('customusers.add_landlord'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
        


class TenantCreateView(View):
    def get(self, request):
        if request.user.is_authenticated and Landlord.objects.filter(user=request.user).exists():
            form = TenantForm()
            return render(request, 'customusers/tenant_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a tenant.')
            return redirect('myadmin:index')

    def post(self, request):
        if request.user.is_authenticated and Landlord.objects.filter(user=request.user).exists():
            form = TenantForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Tenant user created successfully.')
                return redirect('tenant-list')
            else:
                messages.error(request, 'Failed to create tenant. Please check the form.')
                return render(request, 'customusers/tenant_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a tenant.')
            return redirect('myadmin:index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('customusers.add_tenant'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

