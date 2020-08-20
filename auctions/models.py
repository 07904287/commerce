from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    current_bid = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=64)
    photo_URL = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="winner", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Listings'

class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=5, default=0, decimal_places=2)
    
    class Meta:
        verbose_name_plural = 'Bids'

class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Comments'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Watchlist'

    def __str__(self):
        return f"{self.user} {self.listing.id}"