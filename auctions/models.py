from django.contrib.auth.models import AbstractUser
from django.core.validators import  MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='maker')
    title =  models.CharField(max_length = 100)
    description = models.TextField()
    starting_bid = models.IntegerField(validators =[MinValueValidator(0)])
    final_bid = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Categories',on_delete=models.CASCADE, related_name='list_category' )
    image = models.CharField(blank=True, null=True, max_length= 200)
    closed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} {self.title} {self.description} {self.starting_bid} {self.category} {self.image}"

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bid_maker')
    list = models.ForeignKey('Listing', on_delete=models.CASCADE)
    bid = models.IntegerField()

class watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watchlist_user')
    listid = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f"{self.listid} is {self.user} watchlist id"
class Comments(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comment_maker')
    list = models.ForeignKey('Listing', on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user} commented as {self.comment_text}"
