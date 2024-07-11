from django import forms
from .models import Property, PropertyDetails, PropertyImage ,Building


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address', 'building_type', 'number_floors', 'building_age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'building_type': forms.Select(attrs={'class': 'form-control'}),
            'number_floors': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Floors'}),
            'building_age': forms.Select(attrs={'class': 'form-control'}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price' ,'building']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
        }

    def __init__(self, *args, **kwargs):
        self.building_id = kwargs.pop('building_id', None)  # Bina ID'sini alıyoruz
        super().__init__(*args, **kwargs)
        
        # Otomatik olarak bağlı olduğu apartmanı belirlemek için bina ID'sini kullanıyoruz
        if self.building_id:
            self.fields['building'].queryset = Building.objects.filter(id=self.building_id, is_deleted=False)
            self.fields['building'].initial = Building.objects.get(id=self.building_id)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.building_id:
            instance.building_id = self.building_id  # Mülkün bina ID'sini belirliyoruz
        if commit:
            instance.save()
        return instance


class PropertyDetailsForm(forms.ModelForm):
    class Meta:
        model = PropertyDetails
        fields = ['square_meters', 'room_count', 'floor_count', 'furnished', 'balcony', 'elevator', 'parking']
        widgets = {
            'square_meters': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Square Meters'}),
            'room_count': forms.Select(attrs={'class': 'form-control'}),
            'floor_count': forms.Select(attrs={'class': 'form-control'}),
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
