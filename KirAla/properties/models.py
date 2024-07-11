from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError
from customusers.models import Tenant
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()
class Building(models.Model):
    BUILDING_TYPE_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('office', 'Office'),
        ('other', 'Other'),
        ('residential', 'Residential'),
        ('office', 'Office'),
    ]

    BUILDING_AGE_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10+', '10+'),
    ]

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    building_type = models.CharField(max_length=50, choices=BUILDING_TYPE_CHOICES)
    number_floors = models.PositiveIntegerField()
    building_age = models.CharField(max_length=3, choices=BUILDING_AGE_CHOICES)
    is_deleted = models.BooleanField(default=False)
    rental_apartment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def undelete(self):
        self.is_deleted = False
        self.save()

    def update_rental_apartment_count(self):
        self.rental_apartment_count = self.properties.filter(tenant__isnull=False).count()
        self.save()




class Property(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    is_deleted = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.building:
            self.building.update_rental_apartment_count()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def undelete(self):
        self.is_deleted = False
        self.save()

class PropertyDetails(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='details')
    
    ROOM_COUNT_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5+', '5+'),
    ]

    FLOOR_COUNT_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    square_meters = models.PositiveBigIntegerField()
    room_count = models.CharField(max_length=3, choices=ROOM_COUNT_CHOICES)
    floor_count = models.CharField(max_length=3, choices=FLOOR_COUNT_CHOICES)
    furnished = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.title} Details"

class PropertyImage(models.Model):
    property_details = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/properties/')

    def __str__(self):
        return f"Image for {self.property_details.property.title}"
