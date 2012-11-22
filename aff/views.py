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

    return render_to_response('pages/city.html',{'city':city, 'region':region},
                context_instance=RequestContext(request))