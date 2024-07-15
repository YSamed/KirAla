from django.db import models
from properties.models import Apartment ,Building
from customusers.models import Tenant

class Contract(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    is_deleted = models.BooleanField(default=False)  # Yeni alan

    def __str__(self):
        return f"{self.apartment} - {self.tenant}"
