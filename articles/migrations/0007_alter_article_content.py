# Generated by Django 4.0.2 on 2022-02-16 07:18

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_article_content_alter_article_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=30000),
        ),
    ]