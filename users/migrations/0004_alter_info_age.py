# Generated by Django 4.0.2 on 2022-02-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_info_phone_alter_info_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='age',
            field=models.IntegerField(blank=True),
        ),
    ]
