# Generated by Django 4.0.2 on 2022-02-25 12:30

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_info_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
    ]
