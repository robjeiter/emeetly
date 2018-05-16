from django.shortcuts import render
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views import generic
from django.http.response import HttpResponse
import json, requests, random, re
from pprint import pprint
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from emeetlyapp.models import User

#from geopy.geocoders import Nominatim
#import pandas as pd


def coordinates_to_city(fbid, location):
    for component in location['results'][0]['address_components']:
        if 'country' in component['types']:
            country = component['long_name']
            break
    else:
        country = "None"
    for component in location['results'][0]['address_components']:
        if 'postal_town' in component['types']:
            city = component['long_name']
            break
        elif 'locality' in component['types']:
            city = component['long_name']
            break
    else:
        for component in location['results'][0]['address_components']:
            if 'administrative_area_level_2' in component['types']:
                city = component['long_name']
                break
        else:
            city = "None"
    for component in location['results'][0]['address_components']:
        if 'administrative_area_level_1' in component['types']:
            region = component['long_name']
            break
    else:
        region = "None"
    user = User.objects.get(userid=fbid)
    user.city = city
    user.region = region
    user.save()
    pprint(country)
    pprint(city)
    pprint(region)



    """
    geolocator = Nominatim(timeout=3)
    location = geolocator.reverse('51.8700114,-8.480753')
    loc = location.raw
    city = loc['address']['city']
    state = loc ['address']['state']
    pprint(loc)
    pprint(city)
    pprint(state)
    """
