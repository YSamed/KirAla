from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser, Landlord, Tenant
from django import forms


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.startswith('05'):
            raise forms.ValidationError('Phone number must be in the format 05XXXXXXXXX')
        return phone_number


class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.startswith('05'):
            raise forms.ValidationError('Phone number must be in the format 05XXXXXXXXX')
        return phone_number
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        names = first_name.split() 

        for name in names:
            if not name.isalpha():
                raise forms.ValidationError('Should contain only alphabetical characters.')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('Should contain only alphabetical characters.')
        return last_name
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Current Password'
        })

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Password'
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })


class LandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ('business_phone', 'company_name', 'address','business_phone')
        widgets = {
            'business_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_business_phone(self):
        business_phone = self.cleaned_data.get('business_phone')
        if business_phone and not business_phone.isdigit():
            raise forms.ValidationError('Business phone number should consist only of digits.')
        if business_phone and len(business_phone) != 7:
            raise forms.ValidationError('Business phone number must be exactly 7 digits long.')
        return business_phone


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('age', 'national_id', 'employment_status', 'landlord')
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_status': forms.TextInput(attrs={'class': 'form-control'}),
            'landlord': forms.Select(attrs={'class': 'form-control'}),
        }
