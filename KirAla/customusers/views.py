from django.shortcuts import redirect ,render
from django.views.generic import View

from customusers.forms import LandlordForm ,TenantForm ,AdminForm

class CreateUserView(View):
    def get(self, request):
        return render(request, 'customusers/create_user.html')

    def post(self, request):
        user_type = request.POST.get('user_type', 'tenant')
        if user_type == 'landlord':
            return redirect('customusers:create-landlord')
        elif user_type == 'tenant':
            return redirect('customusers:create-tenant')
        elif user_type == 'admin':
            return redirect('customusers:create-admin')
        else:
            return redirect('customusers:create-user')

class LandlordCreateView(View):
    def get(self, request):
        form = LandlordForm()
        return render(request, 'customusers/landlord_create.html', {'form': form})

    def post(self, request):
        form = LandlordForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Handle successful form submission
            return redirect('success-url')  # Replace with your success URL
        return render(request, 'customusers/landlord_create.html', {'form': form})

class TenantCreateView(View):
    def get(self, request):
        form = TenantForm()
        return render(request, 'customusers/tenant_create.html', {'form': form})

    def post(self, request):
        form = TenantForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Handle successful form submission
            return redirect('success-url')  # Replace with your success URL
        return render(request, 'customusers/tenant_create.html', {'form': form})

class AdminCreateView(View):
    def get(self, request):
        form = AdminForm()
        return render(request, 'customusers/admin_create.html', {'form': form})

    def post(self, request):
        form = AdminForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Handle successful form submission
            return redirect('success-url')  # Replace with your success URL
        return render(request, 'customusers/admin_create.html', {'form': form})
