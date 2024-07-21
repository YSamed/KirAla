from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    USER_TYPE_CHOICES = (
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='tenant')

    def __str__(self):
        return self.username


class Landlord(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='landlord')
    business_phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    

class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tenant')
    age = models.IntegerField(blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    employment_status = models.CharField(max_length=50, blank=True, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='tenants')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
