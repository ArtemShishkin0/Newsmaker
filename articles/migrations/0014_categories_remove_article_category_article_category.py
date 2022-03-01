# Generated by Django 4.0.2 on 2022-03-01 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_alter_article_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Other', 'Other'), ('Technologies', 'Technologies'), ('Nature', 'Nature')], default='Other', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(to='articles.Categories'),
        ),
    ]
