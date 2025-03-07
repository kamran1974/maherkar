# Generated by Django 5.1.5 on 2025-02-21 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0002_alter_employer_user_alter_jobseeker_user'),
        ('home_module', '000X_add_tehran_districts'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home_module.tehrandistrict', verbose_name='نام منطقه'),
        ),
    ]
