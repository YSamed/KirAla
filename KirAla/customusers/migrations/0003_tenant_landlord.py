# Generated by Django 4.2.13 on 2024-07-07 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customusers', '0002_alter_tenant_age_alter_tenant_national_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='landlord',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tenants', to='customusers.landlord'),
            preserve_default=False,
        ),
    ]
