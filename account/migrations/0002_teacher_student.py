# Generated by Django 4.1.3 on 2023-12-09 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='ФИО студента')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.user', verbose_name='Преподаватель')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='ФИО студента')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.user', verbose_name='Логин')),
            ],
        ),
    ]
