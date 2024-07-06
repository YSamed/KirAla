from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm
from customusers.models import CustomUser, Landlord ,Tenant

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
def tenant_list(request):
    tenants = Tenant.objects.all()

    context = {
        'tenants': tenants
    }

    return render(request, 'myadmin/tenant_list.html', context)