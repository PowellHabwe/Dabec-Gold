# Generated by Django 3.1.1 on 2023-02-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20230214_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='affordable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='top_rated',
            field=models.BooleanField(default=False),
        ),
    ]
