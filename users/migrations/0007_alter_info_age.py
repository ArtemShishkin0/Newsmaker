# Generated by Django 4.0.2 on 2022-02-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_info_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
