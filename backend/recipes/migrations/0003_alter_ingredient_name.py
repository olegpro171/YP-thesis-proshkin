# Generated by Django 3.2.9 on 2023-08-19 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Название'),
        ),
    ]
