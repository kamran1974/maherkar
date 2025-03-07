# Generated by Django 5.1.5 on 2025-03-01 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0008_employer_county_employer_district_employer_province'),
        ('advertisement_module', '0007_alter_insurance_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertismentjobseeker',
            old_name='type_of_cooperation',
            new_name='insurance',
        ),
        migrations.AddField(
            model_name='advertismentjobseeker',
            name='check_by_admin',
            field=models.BooleanField(default=False, verbose_name=' مشاهده  شده توسط ادمین'),
        ),
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=220, verbose_name='نام مکان')),
                ('job', models.CharField(max_length=220, verbose_name='شغل شما')),
                ('duration', models.CharField(help_text='براساس ماه', max_length=120, verbose_name='مدت زمان')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_histories', to='account_module.jobseeker', verbose_name='کارجو')),
            ],
            options={
                'verbose_name': 'سابقه کار',
                'verbose_name_plural': 'سوابق',
            },
        ),
        migrations.DeleteModel(
            name='Insurance',
        ),
    ]
