# Generated by Django 5.0.7 on 2024-08-14 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_discountcode_options_alter_discountcode_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcode',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
