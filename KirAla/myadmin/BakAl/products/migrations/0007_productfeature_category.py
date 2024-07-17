# Generated by Django 4.2.13 on 2024-07-03 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productfeature_product_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeature',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='products.category'),
            preserve_default=False,
        ),
    ]
