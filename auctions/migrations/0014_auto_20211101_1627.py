# Generated by Django 3.2.8 on 2021-11-01 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0013_auction_last_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ManyToManyField(blank=True, related_name='winners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
