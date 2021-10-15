import datetime
from django.contrib import messages
from django.http import response, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .choices import *

from .models import Listing
from .forms import PostAd

from django.contrib.auth import get_user_model
User = get_user_model()



def index(request):
    listings = Listing.objects.order_by(
        '-list_date', 'verified').filter(is_published=True)

    paginator = Paginator(listings, 10)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    if Listing.verified == True:
        Listing.verified = True
    else:
        Listing.verified = False

    context = {
        'listings': paged_listings,
    }

    return render(request, 'listings/listings.html', context)


@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if Listing.verified == True:
        Listing.verified = True
    else:
        Listing.verified = False
    users = User.objects.all()

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # # Keywords
    # if 'keywords' in request.GET:
    #     keywords = request.GET['keywords']
    #     if keywords:
    #         queryset_list = queryset_list.filter(
    #             description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # # Price
    # if 'price' in request.GET:
    #     price = request.GET['price']
    #     if price:
    #         queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)


@login_required
def ad(request):
    if request.method == "POST":
        form = PostAd(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.landlord = request.user
            post.is_published = True
            post.list_date = datetime.now()
            post.save()
            redirect('/Your Ad listing has been posted', pk=post.listing_id)
    else:
        form = PostAd()
        messages.success(
            request, 'Your Ad has been posted successfully'
        )
    return render(request, 'listings/ad.html', {"form": form})
