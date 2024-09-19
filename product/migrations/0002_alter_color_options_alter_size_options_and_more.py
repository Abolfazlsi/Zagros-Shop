# Generated by Django 5.0.7 on 2024-08-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name': 'رنگ', 'verbose_name_plural': 'رنگ ها'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'اندازه', 'verbose_name_plural': 'اندازه'},
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='products', to='product.size'),
        ),
    ]
