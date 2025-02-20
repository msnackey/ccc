# Generated by Django 5.1.4 on 2024-12-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='google_maps_uri',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='website',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
