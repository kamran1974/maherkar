# Generated by Django 5.1.5 on 2025-03-08 14:19

import django.db.models.deletion
import iranian_cities.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_module', '0001_initial'),
        ('home_module', '0001_initial'),
        ('iranian_cities', '0009_rename_iranian_cit_code_1c3b38_idx_sage_city_code_8db749_idx_and_more'),
        ('jobAndCompanyActivity_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home_module.tehrandistrict', verbose_name='نام منطقه'),
        ),
        migrations.AddField(
            model_name='employer',
            name='province',
            field=iranian_cities.fields.ProvinceField(on_delete=django.db.models.deletion.CASCADE, to='iranian_cities.province', verbose_name='نام استان'),
        ),
        migrations.AddField(
            model_name='employer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='county',
            field=iranian_cities.fields.CountyField(on_delete=django.db.models.deletion.CASCADE, to='iranian_cities.county', verbose_name='نام شهرستان'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home_module.tehrandistrict', verbose_name='نام منطقه'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='job_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobAndCompanyActivity_module.job', verbose_name='شغل'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='province',
            field=iranian_cities.fields.ProvinceField(on_delete=django.db.models.deletion.CASCADE, to='iranian_cities.province', verbose_name='نام استان'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
