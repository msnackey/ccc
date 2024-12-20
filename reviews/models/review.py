from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from cafes.models import Cafe
from reviews.models import Rating
from users.models import User


class ReviewManager(models.Manager):
    """Review manager"""

    pass


class Review(models.Model):
    """Review model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="reviews")
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)

    objects = ReviewManager()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title
