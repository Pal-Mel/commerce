# Generated by Django 3.2.8 on 2021-11-01 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_rates_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]