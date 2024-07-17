# Generated by Django 4.2.13 on 2024-07-16 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customusers', '0004_customuser_user_type_landlord_is_active_and_more'),
        ('contract', '0004_contract_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='landlord',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='customusers.landlord'),
            preserve_default=False,
        ),
    ]
