# Generated by Django 4.1 on 2023-12-11 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_datasets_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='slug',
            field=models.SlugField(max_length=650, null=True),
        ),
    ]
