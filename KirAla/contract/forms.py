from django import forms
from .models import Contract
from properties.models import Apartment
from customusers.models import Tenant

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['apartment', 'tenant', 'start_date', 'end_date', 'rent_amount', 'is_active']
        widgets = {
            'apartment': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            existing_contracts = Contract.objects.values_list('apartment', flat=True)
            self.fields['apartment'].queryset = Apartment.objects.exclude(pk__in=existing_contracts)
        self.fields['tenant'].queryset = Tenant.objects.all() 
