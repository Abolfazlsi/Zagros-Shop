# Generated by Django 5.0.7 on 2024-08-10 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_information_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.SmallIntegerField(),
        ),
    ]
