from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm
from customusers.models import CustomUser, Landlord, Tenant
from customusers.forms import CustomUserUpdateForm,LandlordUpdateForm
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
            # Landlord kontrolü
            if user.groups.filter(name='Landlord').exists():
                login(request, user)
                return redirect('myadmin:index')
            else:
                messages.error(request, 'Bu sayfaya erişim izniniz yok.')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
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

            # Landlord modelini oluştur
            landlord = Landlord.objects.create(user=new_user)
            landlord.save()

            # Oturum aç
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Kayıt işlemi başarıyla tamamlandı.')
                return redirect('myadmin:index')
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'myadmin/register.html', {'form': form})


@login_required
def myadmin_update(request):
    try:
        landlord = request.user.landlord
    except Landlord.DoesNotExist:
        messages.error(request, 'Bu sayfaya erişim izniniz yok.')
        return redirect('myadmin:index')

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        landlord_form = LandlordUpdateForm(request.POST, instance=landlord)
        if user_form.is_valid() and landlord_form.is_valid():
            user_form.save()
            landlord_form.save()
            messages.success(request, 'Bilgileriniz başarıyla güncellendi.')
            return redirect('myadmin:myadmin_update')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        landlord_form = LandlordUpdateForm(instance=landlord)
    
    return render(request, 'myadmin/update.html', {'user_form': user_form, 'landlord_form': landlord_form})



def myadmin_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Şifreniz başarıyla güncellendi!')
            return redirect('myadmin:myadmin_login')
    else:
        form = PasswordChangeForm(request.user)
    
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
