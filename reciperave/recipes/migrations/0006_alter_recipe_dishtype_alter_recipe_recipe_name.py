# Generated by Django 4.0.4 on 2024-08-22 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_delete_recipemedia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='dishType',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipe_name',
            field=models.CharField(max_length=70),
        ),
    ]
