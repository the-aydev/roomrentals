import datetime
from datetime import timezone
from django.contrib import messages
from django.http import response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .choices import *

from .models import Listing
from .forms import PostAd


def index(request):
    listings = Listing.objects.order_by(
        '-list_date').filter(is_published=True)

    paginator = Paginator(listings, 10)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }

    return render(request, 'listings/listings.html', context)


@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

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

    # Bedrooms
    if 'bathroom' in request.GET:
        bathrooms = request.GET['bathroom']
        if bathrooms:
            queryset_list = queryset_list.filter(bedroom__lte=bathrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'garage_choices': garage_choices,
        'garden_choices': garden_choices,
        'air_condition_choices': air_condition_choices,
        'kitchen_choices': kitchen_choices,
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
            post.list_date = timezone.now()
            post.save()
            return response.HttpResponseRedirect('/Your Ad listing has been posted', pk=post.pk)
        else:
            form = PostAd()
    messages.success(
        request, 'Your Ad has been posted successfully'
    )
    return render(request, 'listings/ad.html', {"form": form})


@login_required
def ad(request):
    if request.method == "POST":
        form = PostAd(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            redirect('/Your Ad listing has been posted')
        else:
            return render(request, 'listings/ad.html', {'form': form})
    else:
        form = PostAd()
        messages.success(
            request, 'Your Ad has been posted successfully'
        )
        return render(request, 'listings/ad.html', {"form": form})
    return render(request, 'listings/ad.html', {"form": form})
