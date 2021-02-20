from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User , Listing, Categories, watchlist, Bid, Comments
from .forms import create_page
from django.conf.urls.static import static

class comment_form(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id':'comment_form','placeholder':'comment here!', 'max_length':'255'}), label='')

def index(request):
    lists = Listing.objects.all().order_by('id')
    context = {
        'lists': lists
        }
    return render(request, "auctions/index.html", context)


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

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = create_page(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid =form.cleaned_data['starting_bid']
            category = form.cleaned_data['category']
            image =form.cleaned_data['image']

            user = request.user
            newAuction = Listing.objects.create(
                user = user,
                title = title,
                description = description,
                starting_bid = starting_bid,
                category = category,
                image = image
                )
            return  redirect("index")

    else:
        form = create_page()
        return render(request, 'auctions/create.html',{
            'form': form
        })

def add_watchlist(request, list):
    if request.method == "POST":
        try:
            d = watchlist.objects.get(user=request.user,listid=list)
            d.delete()
        except:
            w = watchlist()
            w.user = request.user
            w.listid = list
            w.save()
        return redirect("index")

@login_required(login_url='/login')
def watchlist_view(request):
    try:
        added = watchlist.objects.filter(user=request.user)
        lists = []
        for i in range(0,len(added)):
            lists.append(Listing.objects.get(id= added[i].listid))

        context = {
                'lists':lists
        }
        return render(request, 'auctions/watchlist.html', context)
    except:
        empty = "Empty, " + "<a href='/'>Home</a>"
        return HttpResponse(empty)

@login_required(login_url='/login')
def list_view(request, list):
    lists = Listing.objects.get(id=list)
    try:
        comments = Comments.objects.filter(list=lists)
        context = {
                'list': lists,
                'comment_form': comment_form,
                'comments': comments
            }
    except:
        context = {
                'list': lists,
                'comment_form': comment_form
            }
    return render(request, 'auctions/list.html', context)

def category_view(request, category):
    category_name = Categories.objects.get(name=category)
    lists = Listing.objects.filter(category=category_name)
    context = {
            'lists':lists
    }
    return render(request, 'auctions/watchlist.html', context)

def take_bid(request, list):
    list_on_bid = Listing.objects.get(id=list)
    current_bid = int(request.POST["current_bid"])
    if current_bid < list_on_bid.starting_bid:
        error = 'You should put a higher Bid, go back to ' + f"<a href='/list/{list}'>List</a>"
        return HttpResponse(error)
    try:
        b = Bid.objects.get(list=list_on_bid)
        l = Listing.objects.get(id=list)
        if b.bid < current_bid:
            b.user = request.user
            b.bid = current_bid
            b.save()
            l.final_bid = current_bid
            l.save()
            home = 'Your Bid is up '+ '<a href="/">Home</a>'
            return HttpResponse(home)
        else:
            error = 'You should put a higher Bid, go back to ' + f"<a href='/list/{list}'>List</a>"
            return HttpResponse(error)
    except:
        b = Bid()
        l = Listing.objects.get(id=list)
        b.user=request.user
        b.list=list_on_bid
        b.bid=current_bid
        b.save()
        l.final_bid = current_bid
        l.save()
        home= 'Your Bid is up'+ '<a href="/">Home</a>'
        return HttpResponse(home)

def addcomment(request, list):
    form = comment_form(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        lists=Listing.objects.get(id=list)
        Comments.objects.create(user=request.user, list=lists, comment_text=text)
        return redirect("index")
    error = "Error Occured, go back to " + f"<a href='/list/{list}'>List</a>"
    return HttpResponse(error)

def close(request, list):
    closed_list = Listing.objects.get(id=list)
    closed_list.closed = True
    closed_list.save()
    return redirect("index")

def delete(request, list):
    w = watchlist.objects.filter(listid=list)
    for i in range(0, len(w)):
        w[i].delete()
    deleted_list = Listing.objects.get(id=list)
    deleted_list.delete()
    return redirect("index")
