import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .choices import *
from .models import Listing
from .forms import PostAd, EditAd
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
    users = User.objects.all()

    context = {
        'listings': paged_listings,
        'users': users,
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
        'listing': listing,
        'users': users,
    }

    return render(request, 'listings/listing.html', context)


class AddListingView(CreateView):
    model = Listing
    form_class = PostAd
    template_name = 'listings/ad.html'


class UpdateListingView(UpdateView):
    model = Listing
    form_class = EditAd
    template_name = 'dashboard/update_ad.html'


class DeleteListingView(DeleteView):
    model = Listing
    template_name = 'dashboard/delete_ad.html'
    success_url = reverse_lazy('home')


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
