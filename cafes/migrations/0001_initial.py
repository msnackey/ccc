# Generated by Django 5.1.4 on 2024-12-29 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('google_place_id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('google_maps_uri', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('rating', models.FloatField(default=0.0)),
                ('number_of_ratings', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
