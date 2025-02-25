# Generated by Django 5.1.5 on 2025-02-16 21:36

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_module', '0001_initial'),
        ('jobAndCompanyActivity_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(help_text='برای مثال 4', verbose_name='روز')),
                ('price', models.IntegerField(help_text='این قیمت کل هست -مثلا برای 7 روز کلا 7000 - قیمت ها به تومان است', verbose_name='قیمت')),
            ],
            options={
                'verbose_name': 'زمان نمایش آگهی',
                'verbose_name_plural': 'زمان نمایش آگهی ها',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220, verbose_name='مهارت های کارجو')),
            ],
            options={
                'verbose_name': 'مهارت',
                'verbose_name_plural': 'مهارت ها',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='نوع اشتراک')),
                ('price', models.IntegerField(default=0, help_text='قیمت ها به تومان است - برای رایگان بودن تعرفه این بخش را نادیده بگیرید', verbose_name='قیمت')),
            ],
            options={
                'verbose_name': 'تعرفه',
                'verbose_name_plural': 'تعرفه ها',
            },
        ),
        migrations.CreateModel(
            name='Advertisment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertise_code', models.CharField(db_index=True, help_text='بعد از ثبت مقدار دهی می شود', max_length=220, unique=True, verbose_name='کدآگهی')),
                ('title', models.CharField(max_length=220, verbose_name='عنوان آگهی')),
                ('description_position', models.TextField(verbose_name='موقعیت شغلی')),
                ('gender', models.CharField(choices=[('مرد', 'مرد'), ('زن', 'زن')], max_length=120, verbose_name='جنسیت')),
                ('soldier_status', models.CharField(choices=[('پایان خدمت', 'پایان خدمت'), ('معافیت دائم', 'معافیت دائم'), ('معافیت تحصیلی', 'معافیت تحصیلی')], max_length=120, verbose_name='وضعیت سربازی')),
                ('degree', models.CharField(choices=[('مهم نیست', 'مهم نیست'), ('زیر دیپلم', 'زیر دیپلم'), ('دیپلم', 'دیپلم'), ('فوق دیپلم', 'فوق دیپلم'), ('لیسانس', 'لیسانس'), ('فوق لیسانس', 'فوق لیسانس'), ('دکترا', 'دکترا')], max_length=120, verbose_name='حداقل مدرک تحصیلی')),
                ('type_of_cooperation', models.CharField(choices=[('مهم نیست', 'مهم نیست'), ('کمتر از 3 سال', 'کمتر از 3 سال'), ('3 تا 6 سال', '3 تا 6 سال'), ('بیشتر از 6 سال', 'بیشتر از 6 سال')], max_length=220, verbose_name='سابقه کار مرتبط')),
                ('salary', models.CharField(help_text='درصورت خالی گذاشتن ای بخش مبلغ دستمزد توافقی می شود', max_length=220, verbose_name='حداقل دستمزد')),
                ('created_at', django_jalali.db.models.jDateTimeField(help_text='بعد از ثبت مقدار دهی می شود', verbose_name='تاریخ ثبت')),
                ('expire_date', django_jalali.db.models.jDateTimeField(blank=True, help_text='به صورت خودکار محاسبه می شود', null=True, verbose_name='تاریخ انقضا')),
                ('total_price', models.IntegerField(default=0, help_text='به صورت خودکار محاسبه می شود', verbose_name='جمع کل')),
                ('pay_status', models.BooleanField(default=False, verbose_name='وضعیت پرداخت')),
                ('check_by_admin', models.BooleanField(default=False, verbose_name=' مشاهده  شده توسط ادمین')),
                ('is_show', models.BooleanField(default=False, verbose_name='نمایش داده شود / نشود')),
                ('status', models.CharField(max_length=220, verbose_name='وضعیت')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='jobAndCompanyActivity_module.job', verbose_name='دسته بندی آگهی')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='account_module.employer', verbose_name='کارفرما')),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='advertisement_module.duration', verbose_name='زمان نمایش')),
                ('skills', models.ManyToManyField(related_name='advertisements', to='advertisement_module.skill', verbose_name='مهارت های کارجو')),
                ('subscribe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='advertisements', to='advertisement_module.subscription', verbose_name='نوع اشتراک')),
            ],
            options={
                'verbose_name': 'آگهی',
                'verbose_name_plural': 'آگهی ها',
            },
        ),
    ]
