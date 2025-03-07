# Generated by Django 5.1.5 on 2025-02-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(help_text='حوزه فعالیت شرکت', max_length=220, unique=True, verbose_name='حوزه فعالیت')),
            ],
            options={
                'verbose_name': 'حوزه فعالیت شرکت',
                'verbose_name_plural': 'حوزه های فعالیت شرکت ها',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_category', models.CharField(help_text='حوزه ای که کارجو در آن فعالیت میکند', max_length=220, unique=True, verbose_name='دسته بندی شغل')),
            ],
            options={
                'verbose_name': 'شغل',
                'verbose_name_plural': 'مشاغل',
            },
        ),
    ]
