# Generated by Django 4.0.2 on 2022-02-14 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, max_length=30000)),
                ('genre', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
