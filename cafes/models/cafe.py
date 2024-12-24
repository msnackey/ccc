from django.db import models


class CafeManager(models.Manager):
    """Cafe manager"""

    pass


class Cafe(models.Model):
    """Cafe model"""

    name = models.CharField(max_length=255)
    google_place_id = models.CharField(max_length=255, unique=True)
    google_maps_uri = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(default=0.0)
    number_of_ratings = models.PositiveBigIntegerField(default=0)

    objects = CafeManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def calc_average_rating(self):
        self.rating = self.ratings.aggregate(models.Avg("rating"))["rating__avg"]
        self.full_clean()
        self.save()

    def calc_number_of_ratings(self):
        self.number_of_ratings = self.ratings.count()
        self.full_clean()
        self.save()
