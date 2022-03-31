from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Auction(models.Model):

    FASHION = "FSHN"
    TOYS = "TOY"
    GADGETS = "GDG"
    CARS = "CAR"
    BOOKS = "BOK"
    MUSIC = "MUS"


    CATEGORY = [
        (FASHION, "Fashion"),
        (TOYS, "Toys"),
        (GADGETS, "Gadgets"),
        (CARS, "Cars"),
        (BOOKS, "Books"),
        (MUSIC, "Music"),
    ]


    title = models.CharField(max_length=128, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    description = models.TextField(blank=False)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    category = models.CharField(max_length=5, choices=CATEGORY, default=FASHION)
    closed = models.BooleanField(default=False)
    image_url = models.URLField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auction Title: {self.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_price}"

class Comment(models.Model):
    aution = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}"


class WatchList(models.Model):
    aution = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.aution}"