from django import forms
from .models import Tenant, Contract 
from properties.models import Building, Apartment


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['apartment', 'tenant', 'start_date', 'end_date', 'rent_amount']
        widgets = {
            'apartment': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.landlord = kwargs.pop('landlord', None)
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            existing_contracts = Contract.objects.values_list('apartment', flat=True)
            
            if self.landlord:
                buildings = Building.objects.filter(landlord=self.landlord)
                self.fields['apartment'].queryset = Apartment.objects.filter(building__in=buildings).exclude(pk__in=existing_contracts)
            else:
                self.fields['apartment'].queryset = Apartment.objects.exclude(pk__in=existing_contracts)
        else:
            self.fields['apartment'].widget.attrs['readonly'] = True

        self.fields['tenant'].queryset = Tenant.objects.all()

    def save(self, commit=True):
        contract = super().save(commit=False)
        
        if self.landlord:
            contract.landlord = self.landlord
        
        if commit:
            contract.save()
        
        return contract