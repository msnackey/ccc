import os

import requests
from django.conf import settings
from django.db import models


class CafeManager(models.Manager):
    """Cafe manager"""

    def get_average_number_of_ratings(self):
        """Gets the average number of ratings across all cafes."""

        if Cafe.objects.exists():
            return Cafe.objects.aggregate(avg=models.Avg("number_of_ratings"))["avg"]
        else:
            return 0

    def get_top_rated_cafes(self, count: int = 5, min_reviews: int = 1):
        """Gets the top rated cafes. 5 cafes are the default."""

        if self.get_average_number_of_ratings() >= 5:
            min_reviews = 5

        return (
            self.get_queryset()
            .filter(number_of_ratings__gte=min_reviews)
            .order_by("-rating", "-number_of_ratings")[:count]
        )

    def get_or_create_from_google(self, google_place_id):
        """Queries the Google Places API to get additional data."""

        cafe, created = self.get_or_create(google_place_id=google_place_id)

        if created:
            api_key = os.getenv("GOOGLE_PLACES_API_KEY")
            url = f"https://places.googleapis.com/v1/places/{google_place_id}?languageCode=nl&fields=*&key={api_key}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                cafe.name = data.get("displayName", {}).get("text", "Unknown Cafe")
                cafe.google_maps_uri = data.get(
                    "googleMapsUri", "Unknown Google Maps Uri"
                )
                cafe.website = data.get("websiteUri", "Unknown Website")
                cafe.address = data.get("formattedAddress", "Unknown Address")
                cafe.latitude = data.get("location", {}).get("latitude", 0.0)
                cafe.longitude = data.get("location", {}).get("longitude", 0.0)
                cafe.save()

                photos = data.get("photos", [])
                try:
                    photo_id = photos[0]["name"]
                    height = photos[0]["heightPx"]
                    width = photos[0]["widthPx"]
                    self.get_google_photo(google_place_id, photo_id, height, width)
                except:
                    print(f"Error fetching photos data for {google_place_id}")
            else:
                error = data.get("error")
                print(
                    f"Error fetching data for Place ID {google_place_id}: {error.get("code")} - {error.get("message")}"
                )

        return cafe

    def get_google_photo(self, google_place_id, photo_id, height, width):
        """Query the Google Places API for a photo."""

        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        url = url = (
            f"https://places.googleapis.com/v1/{photo_id}/media?maxHeightPx={height}&maxWidthPx={width}&skipHttpRedirect=true&key={api_key}"
        )
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            img_data = requests.get(data.get("photoUri")).content
            with open(f"static/img/google/{google_place_id}.jpg", "wb") as handler:
                handler.write(img_data)
        else:
            error = data.get("error")
            print(
                f"Error fetching data for Photo Name {photo_id}: {error.get("code")} - {error.get("message")}"
            )


class Cafe(models.Model):
    """Cafe model"""

    google_place_id = models.CharField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255)
    google_maps_uri = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0, null=True)
    number_of_ratings = models.PositiveBigIntegerField(default=0, null=True)

    objects = CafeManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def calc_average_rating(self):
        self.rating = self.ratings.aggregate(models.Avg("rating"))["rating__avg"]
        # self.full_clean()
        self.save()

    def calc_number_of_ratings(self):
        self.number_of_ratings = self.ratings.count()
        # self.full_clean()
        self.save()
