from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class ProductFeature(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='features')

    def __str__(self):
        return self.name

class FeatureValue(models.Model):
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.feature.name}: {self.value}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/images')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    features = models.ManyToManyField(ProductFeature, blank=True)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.is_active = False
        super().save(*args, **kwargs)

class ProductFeatureValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feature_values')
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.feature.name}: {self.value}'


class Marketing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='marketing_campaigns', blank=True)

    def __str__(self):
        return self.name
    
    def update_products_prices(self):
        if timezone.now().date() <= self.end_date:
            for product in self.products.all():
                original_price = product.price
                discounted_price = original_price * (1 - (self.discount_percentage / 100))
                product.price = discounted_price
                product.save()
        else:
            for product in self.products.all():
                product.price = product.base_price
                product.save()

@receiver(post_save, sender=Marketing)
@receiver(post_delete, sender=Marketing)
def update_products_prices(sender, instance, **kwargs):
    instance.update_products_prices()
