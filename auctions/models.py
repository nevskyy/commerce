from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.username} {self.last_name}"

class Category(models.Model):
    category = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.category}"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

    def __str__(self):
        return f"{self.bid}"
    
class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    initial_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")
    image_url = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    listing_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=True, null=True, related_name="listings")
    watch_list = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist" )
    creating_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    bids = models.ManyToManyField(Bid, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} {self.is_active} {self.creating_date} {self.closing_date}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,  blank=True, null=True, related_name="listingComment")
    comment = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.author} - {self.comment} ({self.date_posted})"
    


