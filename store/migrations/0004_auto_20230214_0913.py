# Generated by Django 3.1.1 on 2023-02-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20230214_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='home_coin',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='home_gold',
            field=models.BooleanField(default=True),
        ),
    ]
