from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Rating


@receiver(post_save, sender=Rating)
def update_rating_on_save(sender, instance, **kwargs):
    """Update average rating when a rating is saved"""
    instance.cafe.calc_average_rating()
    instance.cafe.calc_number_of_ratings()


@receiver(post_delete, sender=Rating)
def update_rating_on_delete(sender, instance, **kwargs):
    """Update average rating when a rating is deleted"""
    instance.cafe.calc_average_rating()
    instance.cafe.calc_number_of_ratings()
