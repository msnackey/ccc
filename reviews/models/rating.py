from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from cafes.models import Cafe
from users.models import User


class RatingManager(models.Manager):
    """Rating manager"""

    pass


class Rating(models.Model):
    """Rating model"""

    class StarRating(models.IntegerChoices):
        ONE = 1, "★"
        TWO = 2, "★★"
        THREE = 3, "★★★"
        FOUR = 4, "★★★★"
        FIVE = 5, "★★★★★"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ratings", blank=False, null=False
    )
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name="ratings", blank=False, null=False
    )
    rating = models.PositiveSmallIntegerField(
        choices=StarRating.choices,
        help_text="Rating between 1 and 5 stars",
        blank=False,
    )
    date = models.DateTimeField(auto_now_add=True)

    objects = RatingManager()

    class Meta:
        ordering = ["-date"]

    @property
    def name(self):
        """Returns a name for the rating"""

        return f"{self.cafe} - {self.rating}"

    def __str__(self):
        return self.get_rating_display()
