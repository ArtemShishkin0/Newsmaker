# Generated by Django 4.0.2 on 2022-03-02 17:56

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=10000),
        ),
    ]