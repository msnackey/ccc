from django.db import models
from django.utils.timezone import now

from cafes.models import Cafe
from reviews.models import Rating
from users.models import User


class ReviewManager(models.Manager):
    """Review manager"""

    def get_recent_reviews(self, count: int = 5):
        """Gets the most recent reviews. 5 reviews are the default."""
        return self.get_queryset()[:count]


class Review(models.Model):
    """Review model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="reviews",
        to_field="google_place_id",
    )
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)

    objects = ReviewManager()

    class Meta:
        ordering = ["-rating__date"]

    def __str__(self):
        return self.title
