from django.db import models
from django.contrib.auth import get_user_model
from other.models import TimeStampedModelMixin

User = get_user_model()

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    is_rented = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

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
    square_meters = models.PositiveBigIntegerField(blank=True, null=True)
    room_count = models.CharField(max_length=3, choices=ROOM_COUNT_CHOICES)
    floor_count = models.CharField(max_length=3, choices=FLOOR_COUNT_CHOICES)
    building_age = models.CharField(max_length=3, choices=BUILDING_AGE_CHOICES)
    number_floors = models.PositiveIntegerField(blank=True, null=True)
    furnished = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    images = models.ImageField(upload_to='images/properties/', blank=True, null=True)

    
    def __str__(self):
        return f"{self.property.title} Details"




