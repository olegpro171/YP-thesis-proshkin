# Generated by Django 3.2.9 on 2023-08-20 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagtorecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_tags', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
