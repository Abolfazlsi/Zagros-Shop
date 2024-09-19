# Generated by Django 5.0.7 on 2024-08-06 20:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]