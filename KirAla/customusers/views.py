from django.shortcuts import render
from .models import Tenant

# Create your views here.











def tenant_list(request):
    tenants = Tenant.objects.all()

    context = {
        'tenants': tenants
    }

    return render(request, 'customer/tenant_list.html', context)