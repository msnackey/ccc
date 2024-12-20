from django.db import models


class CafeManager(models.Manager):
    """Cafe manager"""

    pass


class Cafe(models.Model):
    """Cafe model"""

    name = models.CharField(max_length=255)
    google_place_id = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    objects = CafeManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
