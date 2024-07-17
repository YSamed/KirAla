# Generated by Django 4.2.13 on 2024-07-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_status',
            field=models.CharField(choices=[('pending', 'Beklemede'), ('processing', 'İşleniyor'), ('shipped', 'Kargoya Verildi'), ('completed', 'Tamamlandı'), ('canceled', 'İptal Edildi')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Beklemede'), ('processing', 'İşleniyor'), ('shipped', 'Kargoya Verildi'), ('completed', 'Tamamlandı'), ('canceled', 'İptal Edildi')], default='pending', max_length=20),
        ),
    ]
