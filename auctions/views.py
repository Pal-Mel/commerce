import os
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from auctions.models import *
from django.shortcuts import redirect


from .models import *

from django.contrib.auth.decorators import login_required

def index(request):
    categories = Categori.objects.all()
    if request.method == "POST":
        chooseCat = request.POST['chooseCat'] 
        chooseCatName = "all"
        if chooseCat == "all" :
            auctions = Auction.objects.all()
        else:
            auctions = []
            chooseCatName = Categori.objects.get(id=chooseCat).name
            for auction in Auction.objects.all():
                if len(auction.categori.all().filter(id=chooseCat)) != 0:
                    auctions.append(auction)

        return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':chooseCatName,
            "active":1,
        })
    else:
        categories = Categori.objects.all()
        auctions = Auction.objects.all()
        return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':'all',
            "active":1,
        })

@login_required()

def indexActive(request):
    categories = Categori.objects.all()
    if request.method == "POST":
        chooseCat = request.POST['chooseCat'] 
        chooseCatName = "all"
        if chooseCat == "all" :
            auctions = Auction.objects.filter(status="1")
        else:
            auctions = []
            chooseCatName = Categori.objects.get(id=chooseCat).name
            for auction in Auction.objects.filter(status="1"):
                if len(auction.categori.all().filter(id=chooseCat)) != 0:
                    auctions.append(auction)

        return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':chooseCatName,
            "active":2,
        })
    else:
        auctions = Auction.objects.filter(status="1")
        return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':'all',
            "active":2,
        })

def indexWatchList(request):
    categories = []
    auctions = Auction.objects.filter(status="3")
    return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':'all',
            "active":3,
        })


def getAuction(request,id):
    auction = Auction.objects.get(id=id)
    categories = auction.categori.all()
    return render(request, "auctions/auction.html", {
        'auction':auction,
        'categories':categories
    })