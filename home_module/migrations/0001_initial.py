# Generated by Django 5.1.5 on 2025-03-08 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('iranian_cities', '0009_rename_iranian_cit_code_1c3b38_idx_sage_city_code_8db749_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TehranDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220, unique=True, verbose_name='نام منطقه')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='iranian_cities.city', verbose_name='نام شهر')),
            ],
            options={
                'verbose_name': 'منطقه',
                'verbose_name_plural': 'مناطق',
            },
        ),
    ]
