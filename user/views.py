import os
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from user.models import *
from django.conf import settings

def index(request):
   return render(request, "user/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if len(Profile.objects.filter(user=request.user.id)) != 0:
                profile = Profile.objects.get( user=request.user.id)
                request.session["photoUser"] = os.path.join("..",settings.MEDIA_URL,  profile.photo.url)
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "user/login.html", {
                "message": "Некорректний логін або пароль. Виправте та спробуйте знову."
            })
    else:
        return render(request, "user/login.html")

def login_view_redirect(request, next):
    return HttpResponseRedirect(reverse("user:index"))  

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "user/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("user:index"))
    else:
        return render(request, "user/register.html")
