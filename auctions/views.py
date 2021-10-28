import os
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from auctions.models import *

from .models import *

from django.contrib.auth.decorators import login_required

@login_required()

def index(request):
    categories = Categori.objects.all()
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        'categories':categories,
        'auctions':auctions
    })


def getAuction(request,id):
    auction = Auction.objects.get(id=id)
    categories = auction.categori.all()
    return render(request, "auctions/auction.html", {
        'auction':auction,
        'categories':categories
    })