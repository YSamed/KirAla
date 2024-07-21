
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'admin':
            return function(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('home'))  # Admin yetkisi yoksa ana sayfaya yönlendir
    return wrapper
