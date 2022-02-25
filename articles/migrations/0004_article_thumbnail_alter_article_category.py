# Generated by Django 4.0.2 on 2022-02-15 09:19

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_rename_genre_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=articles.models.PathAndRename('/articleimages')),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Other', 'Other'), ('Technologies', 'Technologies')], default='Other', max_length=100),
        ),
    ]