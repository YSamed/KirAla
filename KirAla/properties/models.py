from django.db import models
from django.contrib.auth.models import User
from other.models import TimeStampedModelMixin


class Property(TimeStampedModelMixin):
    PROPERTY_TYPE_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('other', 'Other'),
    ]

    ROOM_COUNT_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5+'),
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
        ('10', '10+'),
    ]

    SALE_TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    square_meters = models.CharField(max_length=5)
    room_count = models.CharField(max_length=2, choices=ROOM_COUNT_CHOICES)
    number_floors = models.PositiveIntegerField(blank=True, null=True)
    floor_count = models.CharField(max_length=2, choices=FLOOR_COUNT_CHOICES)
    building_age = models.CharField(max_length=2, choices=BUILDING_AGE_CHOICES)
    furnished = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES)
    images = models.ImageField(upload_to='properties_images/', blank=True, null=True)

    def __str__(self):
        return self.title
