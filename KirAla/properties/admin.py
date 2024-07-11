from django.contrib import admin
from .models import Building ,Property, PropertyDetails, PropertyImage

admin.site.register(Building)
admin.site.register(Property)
admin.site.register(PropertyDetails)
admin.site.register(PropertyImage)