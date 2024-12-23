# Generated by Django 5.1.4 on 2024-12-24 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0002_cafe_google_place_id_cafe_latitude_cafe_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='address',
            field=models.CharField(default='asd', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cafe',
            name='google_maps_uri',
            field=models.CharField(default='asd', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cafe',
            name='website',
            field=models.CharField(default='asd', max_length=255),
            preserve_default=False,
        ),
    ]
