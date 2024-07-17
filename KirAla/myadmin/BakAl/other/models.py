from django.db import models
from django.utils import timezone

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Company(TimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    vat_number = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name
