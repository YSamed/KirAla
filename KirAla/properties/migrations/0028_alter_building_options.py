# Generated by Django 4.2.13 on 2024-07-17 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0027_building_landlord'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'permissions': [('properties_add_building', 'Can add building'), ('properties_change_building', 'Can change building'), ('properties_delete_building', 'Can delete building')]},
        ),
    ]
