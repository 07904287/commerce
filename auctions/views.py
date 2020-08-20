from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Comments, Watchlist

CATEGORIES=[
    ('Food', 'Food'),
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ]

class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    starting_bid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Starting Bid'}))
    category =  forms.CharField(label='What is the category of the product?', widget=forms.Select(choices=CATEGORIES))
    photo_URL = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Photo URL'}))

def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listings.objects.all(), 
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, id):
    return render(request, "auctions/listing.html",{
        "listing": Listings.objects.get(id=id),
        "bid": Bids.objects.filter(listing=id).last(),
        "number_of_bids": Bids.objects.filter(listing=id).count(),
        "comments": Comments.objects.filter(listing=id)
    })

@login_required
def bid(request, id):
    if request.method == "POST":
        bid_value = request.POST["bid"]
        l = Listings.objects.get(id=id)
        if float(bid_value) > float(l.current_bid):
            Bids.objects.create(listing=Listings(id),user=User(request.user.id),bid=bid_value)
            l.current_bid = bid_value
            l.save()
        else:
            messages.add_message(request, messages.ERROR, 'Failure to add Bid. Reason: Bid lower than current highest bid.')
        return render(request, "auctions/listing.html",{
        "listing": Listings.objects.get(id=id),
        "bid": Bids.objects.filter(listing=id).last(),
        "number_of_bids": Bids.objects.filter(listing=id).count(),
        "comments": Comments.objects.filter(listing=id)
    })

@login_required
def comment(request, id):
    if request.method == "POST":
        Comments.objects.create(listing=Listings(id),user=User(request.user.id),comment=request.POST["comment"])
        return render(request, "auctions/listing.html",{
        "listing": Listings.objects.get(id=id),
        "bid": Bids.objects.filter(listing=id).last(),
        "number_of_bids": Bids.objects.filter(listing=id).count(),
        "comments": Comments.objects.filter(listing=id)
    })

@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            category = form.cleaned_data["category"]
            photo_URL = form.cleaned_data["photo_URL"]

            l = Listings.objects.create(title=title, description=description, starting_bid=starting_bid, current_bid=starting_bid, category=category, photo_URL=photo_URL, user=request.user, winner=None)

            return HttpResponseRedirect(f"/listings/{l.pk}")
        
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
                "form": NewListingForm()
            })

@login_required
def add_to_watchlist(request, id):
    if Watchlist.objects.filter(listing=Listings(id),user=User(request.user.id)).exists():
        Watchlist.objects.filter(listing=Listings(id),user=User(request.user.id)).delete()
    else:    
        Watchlist.objects.create(listing=Listings(id), user=User(request.user.id))
    
    return render(request, "auctions/listing.html",{
        "listing": Listings.objects.get(id=id),
        "bid": Bids.objects.filter(listing=id).last(),
        "number_of_bids": Bids.objects.filter(listing=id).count(),
        "comments": Comments.objects.filter(listing=id), 
    })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "listings": Watchlist.objects.filter(user=User(request.user.id)), 
    })


def categories(request):
    listings = Listings.objects.all()
    categories = set()
    for listing in listings:
        categories.add(listing.category)

    return render(request, "auctions/categories.html",{
        "categories": categories, 
    })

def specific_category(request, id):
    listings = Listings.objects.filter(category=id)
    return render(request, "auctions/index.html",{
        "listings": listings, 
    })

@login_required
def close(request, id):
    if request.method == "POST":
        l = Listings.objects.get(id=id)
        l.is_active = False
        try: 
            l.winner = Bids.objects.filter(listing=id).last().user
        except AttributeError:
            pass
        l.save()
        

    return render(request, "auctions/index.html",{
        "listings": Listings.objects.all(), 
    })