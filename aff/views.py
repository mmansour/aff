from aff.models import *
from django.contrib.auth.models import User
from cities_light.models import City, Region, Country

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django import forms
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect, HttpResponseRedirect

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _


class LocationForm(forms.Form):
#    logo = forms.ImageField(required=False,)
#    username = forms.CharField(label=_("Create username"), required=True,)
    street_address = forms.CharField(label=_("Address of house to be listed"), required=True,)
    city = forms.CharField(label=_("City"), required=True,)
    region = forms.CharField(label=_("State"), required=True,)


def home(request):
    active_region = ActiveRegion.objects.all()
    return render_to_response('index.html',{'active_region':active_region},
                context_instance=RequestContext(request))


def cities(request, region_slug):
    region = get_object_or_404(Region, slug=region_slug, country__id=234)
    return render_to_response('pages/cities.html',{'region':region},
                context_instance=RequestContext(request))


def city(request, region_slug, city_slug):
    try:
        region = Region.objects.get(slug=region_slug, country__id=234)
        city = region.city_set.get(slug=city_slug)
    except Region.DoesNotExist:
        raise Http404
    except City.DoesNotExist:
        raise Http404

    init_data = {
        'city':city.name,
        'region':region.name,
    }

    form = LocationForm(auto_id=True, initial=init_data)
    if request.method == "POST":
       form = LocationForm(request.POST, auto_id=True)

       if form.is_valid():
           clean_street = form.cleaned_data['street_address']
           clean_city = form.cleaned_data['city']
           clean_state = form.cleaned_data['region']

           request.session['clean_street'] = clean_street
           request.session['clean_city'] = clean_city
           request.session['clean_state'] = clean_state

           redirect = "/account/signup/"
           return HttpResponseRedirect(redirect)

    return render_to_response('pages/city.html',{'city':city, 'region':region, 'form':form},
                context_instance=RequestContext(request))