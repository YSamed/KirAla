from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Landlord, Tenant


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_phone', 'company_name')
    search_fields = ('user__username', 'company_name')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'national_id')
    search_fields = ('user__username', 'national_id')
