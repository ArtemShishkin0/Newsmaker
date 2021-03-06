# Generated by Django 4.0.2 on 2022-03-01 08:43

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_category_remove_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(default='yep', max_length=50, verbose_name=articles.models.Category),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Other', 'Other'), ('Technologies', 'Technologies'), ('Nature', 'Nature')], default='Other', max_length=50),
        ),
    ]
