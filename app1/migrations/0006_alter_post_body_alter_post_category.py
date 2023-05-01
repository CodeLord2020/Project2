# Generated by Django 4.1.7 on 2023-04-28 12:27

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Entertainment', 'Entertainment'), ('Others', 'Others'), ('Politics', 'Politics'), ('Programming', 'Programming'), ('Sport', 'Sport'), ('Technology', 'Technology'), ('Others', 'Others')], default='Others', max_length=100),
        ),
    ]