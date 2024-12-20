from django.db import models


class CafeManager(models.Manager):
    """Cafe manager"""

    pass


class Cafe(models.Model):
    """Cafe model"""

    name = models.CharField(max_length=255, blank=False)

    objects = CafeManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
