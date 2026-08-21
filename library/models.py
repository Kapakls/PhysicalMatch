from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    spotify_id = models.CharField(max_length=200, unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=2, blank=True)
    profile_url = models.URLField(blank=True)
    profile_image = models.URLField(blank=True)


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_date = models.DateField()
    spotify_id = models.CharField(max_length=200, unique=True)
    artwork = models.URLField(max_length=500)


class UserAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="users")

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["user", "album"],
                name="unique_user_album",
            ),
        )


class DiscogsMarketplaceListing(models.Model):
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="discogs_marketplace_listings"
    )
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    listing_id = models.CharField(max_length=200, unique=True)
    listing_url = models.URLField(blank=True)
    media_condition = models.CharField(max_length=200)
    sleeve_condition = models.CharField(max_length=200)
    seller_country = models.CharField(max_length=2)
    seller_rating = models.DecimalField(max_digits=5, decimal_places=2)
