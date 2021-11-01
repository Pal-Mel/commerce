import os
from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.forms import ModelForm
from auctions.models import *
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages




from .models import *

from django.contrib.auth.decorators import login_required

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = '__all__'
        exclude = ['createdate', 'status', 'user']



def index(request):
    watchList=[]
    if request.user.is_authenticated:
        wList = WatchAuction.objects.filter(user = request.user)
        for el in wList:
            watchList.append(el.auction.id)
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
            "watchList":watchList
        })
    else:
        categories = Categori.objects.all()
        auctions = Auction.objects.all()
        return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':'all',
            "active":1,
            "watchList":watchList
        })

@login_required()

def indexActive(request):
    watchList=[]
    wList = WatchAuction.objects.filter(user = request.user)
    for el in wList:
        watchList.append(el.auction.id)
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
            "watchList":watchList
        })
    else:
        auctions = Auction.objects.filter(status="1")
        return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':'all',
            "active":2,
            "watchList":watchList
        })

@login_required()

def indexWatchList(request):
    categories = []
    watchList = WatchAuction.objects.filter(user = request.user)
    auctions =[]
    for el in watchList:
        auctions.append(el.auction)
    return render(request, "auctions/index.html", {
            'categories':categories,
            'auctions':auctions,
            'currentCat':'all',
            "active":3,
        })

@login_required()

def addWatch(request,id):
    if request.method == "POST":
        auction = Auction.objects.get(id=id)
        list = WatchAuction.objects.filter(user=request.user, auction = auction)
        if len(list.all()) == 0:
            WatchAuction.objects.create(user=request.user, auction = auction)
        else:
            list.delete()
        return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))
    return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))


@login_required()

def closeAuction(request,id):
    auction = Auction.objects.get(id=id)
    rates = Rates.objects.filter(auction=auction).order_by('-rate').all()

    if request.method == "POST":
        if auction.user.id == request.user.id:
            if len(rates) != 0:
                auction.status = Status.objects.get(id=2)
                auction.last_rate = rates[0].rate
                auction.save()
                AuctionWinner.objects.create(user = rates[0].user, auction=auction, rate=rates[0].rate)
                if request.user == rates[0].user:
                    messages.info(request, f'Ви виграли у цьому ауціоні. Зв’яжіться з продавцем для отримання товару.') 

        return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))

    return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))

@login_required()

def makeRate(request,id, minRate):
    if request.method == "POST":
        auction = Auction.objects.get(id=id)
        youRate = request.POST["youRate"]
        if float(youRate) > float(minRate):
            Rates.objects.create(rate=float(youRate), auction=auction, user=request.user)
            auction.last_rate = youRate
            auction.save()
            return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))
        else:
            messages.warning(request, f'Ставка має бути більша за {minRate}')    
    return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))

@login_required()

def addAuction(request):
    if request.method == "POST" :
        if request.FILES :
            form = AuctionForm(request.POST,  request.FILES)
        else:
            form = AuctionForm(request.POST)
        if form.is_valid() :
            a = Auction()
            a.name = form.cleaned_data['name']
            a.description = form.cleaned_data['description']
            a.first_rate = form.cleaned_data['first_rate']
            a.user=request.user
            a.status=Status.objects.get(id=1)
            a.image=form.cleaned_data['image']
            a.save()
            b = Auction.objects.get(id = a.id)
            b.categori.set(form.cleaned_data['categori'])
            b.save()
            return HttpResponseRedirect(reverse("auction:index"))

        else:
            return render(request, "auctions/add.html", {
            "form": form
            })
    return render(request, "auctions/add.html",{
        "form":AuctionForm,
    })

@login_required()

def comment(request,id):
    if request.method == "POST":
        comment = request.POST["comment"].strip()
        if comment != "":
            auction = Auction.objects.get(id=id)
            Comments.objects.create(comment=comment, auction=auction, user=request.user)
        return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))
    return HttpResponseRedirect(reverse('auction:getAuction', kwargs={"id":id}))

def getAuction(request,id):
    auction = Auction.objects.get(id=id)
    categories = auction.categori.all()
    comments = Comments.objects.filter(auction=auction).order_by("-date")
    if request.user.is_authenticated:
        list = WatchAuction.objects.filter(user=request.user, auction = auction)
        if len(list.all()) == 0:
            inWatch = False
        else:
            inWatch = True
        rates = Rates.objects.filter(auction=auction).order_by('-rate').all()
        if len(rates) == 0:
            minRate = auction.first_rate
        else:
            minRate = rates[0].rate
        w = AuctionWinner.objects.filter(auction=auction)
        if len(w.all()) != 0:
            winner =w.all()[0].user
            if winner == request.user:
                messages.info(request, f'Ви виграли у цьому ауціоні. Зв’яжіться з продавцем для отримання товару.') 
        else:
            winner = ''
        return render(request, "auctions/auction.html", {
            'auction':auction,
            'categories':categories,
            'inWatch':inWatch,
            'minRate':minRate,
            'rates':rates,
            "winner": winner,
            "comments": comments
        })
    else:
        return render(request, "auctions/auction.html", {
            'auction':auction,
            'categories':categories,
            "comments": comments,
        })