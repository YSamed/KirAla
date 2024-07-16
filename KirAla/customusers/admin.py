from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Landlord, Tenant

admin.site.register(CustomUser)


@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_phone', 'company_name')
    search_fields = ('user__username', 'company_name')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'national_id')
    search_fields = ('user__username', 'national_id')
