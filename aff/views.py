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
import os


def home(request):

    active_region = ActiveRegion.objects.all()

######Interesting but not needed
#    active_region = [ar.region for ar in ActiveRegion.objects.all()]
#    for r in country.region_set.all():
#        if r.name in active_region:
#            print r.name

#    country = Country.objects.get(id=234) #USA
#    for c in country.city_set.filter(region__name='California'): # HOW TO GRAB ALL CITIES IN A STATE
#        print c

    return render_to_response('index.html',{'active_region':active_region},
                context_instance=RequestContext(request))