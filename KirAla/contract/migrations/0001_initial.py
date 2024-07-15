# Generated by Django 4.2.13 on 2024-07-14 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customusers', '0003_tenant_landlord'),
        ('properties', '0026_building_floors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('rent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='properties.apartment')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='customusers.landlord')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='customusers.tenant')),
            ],
        ),
    ]
