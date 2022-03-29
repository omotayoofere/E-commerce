from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import models
from . import forms


def index(request):

    auction = models.Auction.objects.all()
    context = {
        "auction": auction
    }
    return render(request, "auctions/index.html", context=context)


def create_listing(request):
    if request.method == "POST":
        form = forms.AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/create_list.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create_list.html", {
            "form": forms.AuctionForm()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def auction_details(request, pk):
    try:
        auction = models.Auction.objects.get(pk=pk)
        
    except models.Auction.DoesNotExist:
        return render(request, 'auctions/404.html')

    return render(request, 'auctions/auction_detail.html', context={'auction': auction})