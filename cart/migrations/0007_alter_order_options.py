# Generated by Django 5.0.7 on 2024-08-14 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_order_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('created_at',), 'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
    ]
