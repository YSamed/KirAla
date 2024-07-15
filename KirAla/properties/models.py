from django.db import models
from customusers.models import Landlord 


class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='buildings')

    
    BUILDING_TYPES = [
        ('apart', 'Apart'),
        ('apartment', 'Apartman'),
        ('office', 'Ofis'),
        ('house', 'Ev'),
        ('villa', 'Villa'),
        ('other', 'Diğer'),
    ]
    building_type = models.CharField(max_length=10, choices=BUILDING_TYPES)
    
    building_age = models.PositiveIntegerField()
    floors = models.PositiveIntegerField()
    
    rental_apartment_count = models.PositiveIntegerField(default=0) ### UNUTMA
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Apartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
    number = models.CharField(max_length=10)
    floor = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    area = models.DecimalField(max_digits=8, decimal_places=2)
    is_rented = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/apartment/')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.building.name} - Daire {self.number}"
