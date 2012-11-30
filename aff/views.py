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

######################################### FORMS
class LocationForm(forms.Form):
#    logo = forms.ImageField(required=False,)
#    username = forms.CharField(label=_("Create username"), required=True,)
    street_address = forms.CharField(label=_("Address of house to be listed"), required=True,)
    city = forms.CharField(label=_("City"), required=True,)
    region = forms.CharField(label=_("State"), required=True,)


class PropertyDescriptionForm(forms.Form):
    square_feet = forms.CharField(label=_("Square footage"), required=True,)
    number_of_bedrooms = forms.CharField(label=_("Number of bedrooms"), required=True,)
    number_of_bathrooms = forms.CharField(label=_("Number of bathrooms"), required=True,)


class ImageForm(forms.Form):
    propertyimage = forms.ImageField(required=False,)


######################################### VIEWS
def home(request):
    active_region = ActiveRegion.objects.all()
    return render_to_response('index.html',{'active_region':active_region},
                context_instance=RequestContext(request))


def cities(request, region_slug):
    region = get_object_or_404(Region, slug=region_slug, country__id=234)
    return render_to_response('pages/cities.html',{'region':region},
                context_instance=RequestContext(request))


def propertyimages(request, property_id):
    init_data = {
#        'city':city.name,
#        'region':region.name,
    }

    property = PropertyDescription.objects.get(id=property_id)

    form = ImageForm(auto_id=True, initial=init_data)
    if request.method == "POST":
       form = ImageForm(request.POST, request.FILES, auto_id=True)
       if form.is_valid():
            #do stuff
            propertyimage = PropertyImage(
                img = form.cleaned_data['propertyimage'],
                property = property
            )

            propertyimage.save()

            redirect = '{0}'.format(request.path)
            return HttpResponseRedirect(redirect)
    return render_to_response('pages/propertyimages.html',{'property':property, 'form':form},
                context_instance=RequestContext(request))



def propertydescription(request):

    init_data = {
#        'city':city.name,
#        'region':region.name,
    }

    form = PropertyDescriptionForm(auto_id=True, initial=init_data)
    if request.method == "POST":
       form = PropertyDescriptionForm(request.POST, auto_id=True)
       if form.is_valid():
            #do stuff
            property = PropertyDescription(
                title="{0} {1} {2}".format(request.session['clean_street'],request.session['clean_city'],request.session['clean_state']),
                address1=request.session['clean_street'],
                city=request.session['clean_city'],
                state=request.session['clean_state'],
                square_feet=form.cleaned_data['square_feet'],
                number_of_bedrooms=form.cleaned_data['number_of_bedrooms'],
                number_of_bathrooms=form.cleaned_data['number_of_bathrooms'],
                user = request.user
            )

            property.save()

            redirect = "/propertyimages/{0}/".format(property.id)
            return HttpResponseRedirect(redirect)
    return render_to_response('pages/propertydescription.html',{'form':form},
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

           redirect = "/account/signup/?next=/propertydescription/"
           return HttpResponseRedirect(redirect)

    return render_to_response('pages/city.html',{'city':city, 'region':region, 'form':form},
                context_instance=RequestContext(request))