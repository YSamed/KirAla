from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import LandlordForm, TenantForm
from .models import Landlord

class CreateUserView(View):
    def get(self, request):
        return render(request, 'customusers/create_user.html')

    def post(self, request):
        user_type = request.POST.get('user_type', 'tenant')
        if user_type == 'landlord':
            return redirect('customusers:create-landlord')
        elif user_type == 'tenant':
            return redirect('customusers:create-tenant')
        else:
            return redirect('customusers:create-user')


class LandlordCreateView(View):
    def get(self, request):
        if request.user.is_authenticated and Landlord.objects.filter(user=request.user, is_admin=True).exists():
            form = LandlordForm()
            return render(request, 'customusers/landlord_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a landlord.')
            return redirect('customusers:create-user')
    
    def post(self, request):
        if request.user.is_authenticated and Landlord.objects.filter(user=request.user, is_admin=True).exists():
            form = LandlordForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Landlord user created successfully.')
                return redirect('admin-list')  
            else:
                messages.error(request, 'Failed to create landlord. Please check the form.')
                return render(request, 'customusers/landlord_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a landlord.')
            return redirect('customusers:create-user')
        

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
                return redirect('admin-list')
            else:
                messages.error(request, 'Failed to create tenant. Please check the form.')
                return render(request, 'customusers/tenant_create.html', {'form': form})
        else:
            messages.error(request, 'You do not have permission to create a tenant.')
            return redirect('myadmin:index')

