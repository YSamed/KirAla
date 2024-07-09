from django import forms
from .models import Property, PropertyDetails, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'property_type', 'location', 'price', 'is_rented']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'is_rented': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PropertyDetailsForm(forms.ModelForm):
    class Meta:
        model = PropertyDetails
        fields = ['square_meters', 'room_count', 'floor_count', 'building_age', 'number_floors', 'furnished', 'balcony', 'elevator', 'parking']
        widgets = {
            'square_meters': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Square Meters'}),
            'room_count': forms.Select(attrs={'class': 'form-control'}),
            'floor_count': forms.Select(attrs={'class': 'form-control'}),
            'building_age': forms.Select(attrs={'class': 'form-control',}),
            'number_floors': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Floors'}),
            'furnished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'elevator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
