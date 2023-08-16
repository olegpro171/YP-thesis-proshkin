# Generated by Django 3.2.3 on 2023-08-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230816_1113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredienttorecipe',
            options={'verbose_name': 'Ингридиенты в рецептах', 'verbose_name_plural': 'Ингридиенты в рецептах'},
        ),
        migrations.AlterModelOptions(
            name='tagtorecipe',
            options={'verbose_name': 'Теги в рецептах', 'verbose_name_plural': 'Теги в рецептах'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipes/image/', verbose_name='Изображение'),
        ),
    ]