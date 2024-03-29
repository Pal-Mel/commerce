from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import related
from django.conf import settings


class Categori(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    


class Status(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Auction(models.Model):
    name = models.CharField(max_length=150)
    categori=models.ManyToManyField(Categori, blank=True, related_name="categories")
    description=models.TextField()
    first_rate=models.FloatField()
    image=models.ImageField(upload_to='images_auctions/%Y/%m/%d', null=True, blank=True)
    status=models.ForeignKey(Status,on_delete=models.DO_NOTHING)
    createdate= models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    last_rate=models.FloatField(default=0)

    def __str__(self):
        return f"{self.name }, початкова вартість {self.first_rate} ({self.createdate}) - {self.status}"

class AuctionWinner(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    auction=models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    rate=models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True,  blank=True)


class WatchAuction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.auction.name} - ({self.user.username})"

class Rates(models.Model):
    auction=models.ForeignKey(Auction,on_delete=models.DO_NOTHING,related_name="rate_auctions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    rate=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction }, ставка {self.rate} ({self.date})"

class Comments(models.Model):
    auction=models.ForeignKey(Auction,on_delete=models.DO_NOTHING,related_name="auction_comments")
    comment=models.TextField(max_length=255)
    date=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="user_comments")

    def __str__(self):
        return f"{self.auction } - {self.comment} ({self.date, self.user})"