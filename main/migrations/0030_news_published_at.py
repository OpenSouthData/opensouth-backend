# Generated by Django 4.1 on 2024-02-03 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_datasets_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
