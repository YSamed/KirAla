# Generated by Django 4.2.13 on 2024-07-16 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customusers', '0004_customuser_user_type_landlord_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('landlord', 'Landlord'), ('tenant', 'Tenant')], default='tenant', max_length=10),
        ),
    ]
