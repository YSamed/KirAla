from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth.models import Group
from customusers.models import Landlord, Tenant
from customusers.forms import CustomUserRegistrationForm, CustomUserUpdateForm, LandlordForm, TenantForm, CustomPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def index(request):
    return render(request, 'myadmin/index.html')

def myadmin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.user_type == 'landlord':
                login(request, user)
                return redirect('myadmin:index')
            elif user.user_type == 'admin':
                login(request, user)
                return redirect('myadmin:index')
            else:
                messages.error(request, 'You do not have access to this page.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'myadmin/login.html')

@login_required
def myadmin_logout(request):
    logout(request)
    return redirect('myadmin:myadmin_login')

def myadmin_register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            landlord_group, created = Group.objects.get_or_create(name='Landlord')
            new_user.groups.add(landlord_group)

            landlord = Landlord.objects.create(user=new_user)
            landlord.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successfully completed.')
                return redirect('myadmin:index')
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'myadmin/register.html', {'form': form})

@login_required
def myadmin_update(request):
    try:
        landlord = request.user.landlord
    except Landlord.DoesNotExist:
        messages.error(request, 'You do not have access to this page.')
        return redirect('myadmin:index')

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        landlord_form = LandlordForm(request.POST, instance=landlord)
        if user_form.is_valid() and landlord_form.is_valid():
            user_form.save()
            landlord_form.save()
            messages.success(request, 'Your information has been successfully updated.')
            return redirect('myadmin:myadmin_update')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        landlord_form = LandlordForm(instance=landlord)
    
    return render(request, 'myadmin/update.html', {'user_form': user_form, 'landlord_form': landlord_form})

@login_required
def myadmin_password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password has been successfully updated! Şifreniz başarıyla güncellendi!')
            return redirect('myadmin:myadmin_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'myadmin/password_change.html', {'form': form})

@login_required
def tenant_list(request):
    if request.user.groups.filter(name='Landlord').exists():
        landlord = request.user.landlord
        tenants = Tenant.objects.filter(landlord=landlord)
    else:
        tenants = Tenant.objects.none()

    context = {
        'tenants': tenants
    }

    return render(request, 'myadmin/tenant_list.html', context)
