# Generated by Django 5.0.6 on 2024-10-31 07:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_login_login_date_login_login_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='login_date',
        ),
        migrations.RemoveField(
            model_name='login',
            name='login_time',
        ),
        migrations.RemoveField(
            model_name='student',
            name='signup_date',
        ),
        migrations.RemoveField(
            model_name='student',
            name='signup_time',
        ),
        migrations.AddField(
            model_name='login',
            name='login_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='student',
            name='signup_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
