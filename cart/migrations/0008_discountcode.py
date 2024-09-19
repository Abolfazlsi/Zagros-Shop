# Generated by Django 5.0.7 on 2024-08-14 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_order_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('discount', models.SmallIntegerField(default=0)),
                ('quantity', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
