# Generated by Django 3.2.9 on 2023-08-19 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='datetime',
        ),
    ]
