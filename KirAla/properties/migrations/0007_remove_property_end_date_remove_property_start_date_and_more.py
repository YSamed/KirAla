# Generated by Django 4.2.13 on 2024-07-08 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_propertydetails_balcony_propertydetails_elevator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='property',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='property',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='property',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='propertydetails',
            name='property',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='properties.property'),
        ),
    ]
