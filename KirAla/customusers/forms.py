from django import forms
from .models import CustomUser ,Landlord

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name' , 'email', 'phone_number']


class LandlordUpdateForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ['company_name','business_phone','address']
