# Generated by Django 4.2.13 on 2024-07-04 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='owner',
        ),
    ]
