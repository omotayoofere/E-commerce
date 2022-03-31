from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import models
from . import forms


def index(request):

    auction = models.Auction.objects.all()

    if auction['closed'] == False:
        return render(request, "auctions/index.html", context=auction)
    else:
        return render(request, "auctions/closed.html", context=auction)


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

    #get the auction
    #get the bid_price
    #get bid_comment
    #get the current highest bid_price
    #check watchlist 
    #get the comment associated with aution
    #if aution is closed, user with highest bid_price = winner
    #provide different view if user that makes request is the seller, 
    #create different scenario for other categories; winner and other users
    #Render BidForm, CommentForm

    try:
        auction = models.Auction.objects.get(pk=pk)

    except models.Auction.DoesNotExist:
        return render(request, 'auctions/error_handling.html', {
            "code": 404,
            "message": "Auction id was not found"
        })

    bid_count = models.Bid.objects.get(auction=pk).count()
    highest_bidder = models.Bid.objects.get(auction=pk).order_by('-bid_price').first()

    if auction.closed:
        if highest_bidder is not None:
            winner = highest_bidder.user

            if request.user.id == auction.created_by.id:
                return render(request, 'auctions/items_sold.html', {
                    "auction": auction
                })
            elif request.user.id == winner.id:
                return render(request, 'auctions/items_bought.html', {
                    "auction": auction,
                    "winner": winner
                })
            else:
                return render(request, 'auctions/closed.html', {
                    "auction": auction})
        else:
            if request.user.id == auction.created_by.id:
                return render(request, 'auctions/no_offer.html', {
                    "auction": auction
                })

    else:
        if request.user.is_authenticated:
            watchlist_item = models.WatchList.objects.filter(aution=pk, user=models.User.objects.get(id=request.user.id)).first()

            if watchlist_item is not None:
                on_watchlist = True
            else:
                on_watchlist = False
        else:
            on_watchlist = False

        comments = models.Comment.objects.filter(aution=pk)

        if highest_bidder is not None:
            if highest_bidder.user == request.user.id:
                bid_message = "Your bid id the highest bid"
            else:
                bid_message = f"Highest bid made by: {highest_bidder.user.username}"
        else:
            bid_message = None


    bid = forms.BidForm()
    comment = forms.CommentForm()



    context = {
        "bid_count": bid_count,
        "comments": comments,
        "bid_message": bid_message,
        "on_watchlist": on_watchlist,
        "bid": bid, 
        "comment": comment
    }

    return render(request, 'auctions/auction_detail.html', context=context)