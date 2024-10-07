from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "categories": Category.objects.all(),
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        bid = request.POST['bid']
        img_url = request.POST['imageUrl']
        category = request.POST['category']
        current_user = request.user

        category_data = Category.objects.get(category=category)

        bid = Bid(bid=Decimal(bid), user=current_user)
        bid.save()

        listing = Listing.objects.create(
            title=title, 
            description=description, 
            initial_bid=bid, 
            image_url=img_url, 
            category=category_data,
            listing_owner=current_user)
        
        listing.save()

        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        categories = Category.objects.all()

        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })
    
def select_listing(request, listing_id):
    listing_data = Listing.objects.get(pk=listing_id)
    current_user = request.user
    # is_listing_in_watchlist = listing_data.watch_list.filter(id=current_user.id).exists()
    is_listing_in_watchlist = current_user in listing_data.watch_list.all()
    comments = Comment.objects.filter(listing=listing_data)
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "isListingInWatchlist": is_listing_in_watchlist,
        "comments": comments,
    })

def remove_listing(request, listing_id):
    listing_data = Listing.objects.get(pk=listing_id)
    current_user = request.user
    listing_data.watch_list.remove(current_user)
    
    return HttpResponseRedirect(reverse('auctions:select_listing', args=[listing_id]))

def add_listing(request, listing_id):
    listing_data = Listing.objects.get(pk=listing_id)
    current_user = request.user
    listing_data.watch_list.add(current_user)
    
    return HttpResponseRedirect(reverse('auctions:select_listing', args=[listing_id]))

def show_active_listings_by_category(request):
    if request.method == "POST":
        category = request.POST["category"]
        categories = Category.objects.all()
        selected_category = Category.objects.get(category=category)
        active_listings = Listing.objects.filter(category=selected_category, is_active=True)

        return render(request, "auctions/listings_by_category.html", {
            "active_listings": active_listings,
            "categories": categories,
            "selected_category": selected_category,
        })
    else:
        categories = Category.objects.all()

        return render(request, "auctions/listings_by_category.html", {
            "categories": categories
        })
    
def show_watch_list(request):
    current_user = request.user
    user_watch_list = current_user.watchlist.all()

    print(user_watch_list)

    return render(request, "auctions/watch_list.html", {
        "userWatchList": user_watch_list
    })

def add_comment(request, listing_id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=listing_id)
    comment = request.POST['new_comment']
    
    new_comment = Comment(
        author = current_user,
        listing = listing_data,
        comment = comment,
    )

    new_comment.save()

    return HttpResponseRedirect(reverse('auctions:select_listing', args=[listing_id]))
