# Generated by Django 5.0.6 on 2024-12-29 17:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=60)),
                ('login_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=10)),
                ('password1', models.CharField(max_length=128)),
                ('password2', models.CharField(max_length=128)),
                ('signup_time', models.TimeField()),
                ('signup_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
