# Generated by Django 5.0.7 on 2024-08-05 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_otp_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='نام و نام خانوادگی'),
        ),
    ]
