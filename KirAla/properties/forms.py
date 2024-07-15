from django import forms
from .models import Building , Apartment

# Building Form
class BuildingForm(forms.ModelForm):
    FLOOR_CHOICES = [(i, str(i)) for i in range(1, 51)]
    floors = forms.ChoiceField(choices=FLOOR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    BUILDING_AGE_CHOICES = [(i, str(i)) for i in range(1, 51)]
    building_age = forms.ChoiceField(choices=BUILDING_AGE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Building
        fields = ['name', 'address', 'building_type', 'floors', 'building_age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'building_type': forms.Select(attrs={'class': 'form-control'}),
            'floors': forms.Select(attrs={'class': 'form-control'}),
            'building_age': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean_floors(self):
        floors = self.cleaned_data.get('floors')
        if floors is not None and int(floors) < 0:
            raise forms.ValidationError("Please enter a positive number.")
        return floors

    def clean_building_age(self):
        building_age = self.cleaned_data.get('building_age')
        if building_age is not None and int(building_age) < 0:
            raise forms.ValidationError("Please enter a positive number.")
        return building_age


# Apartment Form
class ApartmentForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)

    class Meta:
        model = Apartment
        fields = ['number', 'floor', 'rooms', 'area', 'is_rented', 'furnished', 'balcony', 'elevator', 'parking', 'image']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment Number'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Floor'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Rooms'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area'}),
            'is_rented': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'furnished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'elevator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }

        labels = {
            'number': 'Apartment Number',
            'rooms': 'Number of Rooms',
            'is_rented': 'Is Rented',
            'furnished': 'Furnished',
            'balcony': 'Balcony',
            'elevator': 'Elevator',
            'parking': 'Parking',
            'image': 'Apartment Image',
        }

    def clean_floor(self):
        floor = self.cleaned_data.get('floor')
        if floor is None or floor <= 0:
            raise forms.ValidationError("Floor must be greater than zero.")
        return floor

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area is None or area <= 0:
            raise forms.ValidationError("Area must be greater than zero.")
        return area
    
    @property
    def is_rented(self):
        return self.contracts.filter(is_active=True).exists()
