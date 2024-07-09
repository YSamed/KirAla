from django.contrib import admin
from .models import Property, PropertyDetails, PropertyImage

admin.site.register(Property)
admin.site.register(PropertyDetails)
admin.site.register(PropertyImage)