from django import forms
from .models import Property, PropertyDetails

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'price', 'property_type', 'is_rented']


class PropertyDetailsForm(forms.ModelForm):

    class Meta:
        model = PropertyDetails
        fields = ['room_count', 'floor_count', 'building_age', 'number_floors', 'square_meters', 'furnished', 'balcony', 'elevator', 'parking','images']
