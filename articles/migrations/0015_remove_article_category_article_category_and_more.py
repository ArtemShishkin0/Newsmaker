# Generated by Django 4.0.2 on 2022-03-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_categories_remove_article_category_article_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Other', 'Other'), ('Technologies', 'Technologies'), ('Nature', 'Nature')], default='Other', max_length=100),
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
    ]