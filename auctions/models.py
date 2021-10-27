from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import related

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
    categori=models.ForeignKey(Categori,on_delete=models.PROTECT,related_name="categories")
    description=models.TextField()
    first_rate=models.FloatField()
    image=models.ImageField(upload_to='images/', null=True, blank=True)
    status=models.ForeignKey(Status,on_delete=models.PROTECT,related_name="auction_statuses")
    createdate= models.DateTimeField()
    user=models.CharField(max_length=150) #ManyToOneRel(User, field_name="'id'", to="'id'")

    def __str__(self):
        return f"{self.name }, початкова вартість {self.first_rate} ({self.createdate}) - {self.status}"

class Rates(models.Model):
    auction=models.ForeignKey(Auction,on_delete=models.DO_NOTHING,related_name="rate_auctions")
    user=models.CharField(max_length=150)#ManyToManyField(User,blank=False,related_name="user_rates")
    rate=models.FloatField()
    date=models.DateTimeField()

    def __str__(self):
        return f"{self.auction }, ставка {self.rate} ({self.date})"

class Comments(models.Model):
    auction=models.ForeignKey(Auction,on_delete=models.DO_NOTHING,related_name="auction_comments")
    comment=models.TextField(max_length=350)
    date=models.DateTimeField()
    user=models.CharField(max_length=150) #ManyToManyField(User,blank=False)

    def __str__(self):
        return f"{self.auction } - {self.comment} ({self.date, self.user})"