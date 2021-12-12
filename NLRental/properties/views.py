from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
from django import forms
from django.db.models import Avg
 # Create your views here.

import json

from WebEng.NLRental.properties.models import Property

//properties data imported as 'Data'

# with open('/Users/khanakgulati/Downloads/archive/properties.json') as f:
# 	data = json.load(f)

# resp = requests.get('/Users/khanakgulati/Downloads/archive/properties.json')


def index(request):
	# requests = Request.objects.all()
	# resp = requests.get('properties.json')
    return render(request, "index.html")
	# , {
	# 	'response': resp})
		
	# 	requests.get('https://www.kaggle.com/juangesino/netherlands-rent-properties?select=properties.json').json()
	# })

def create_property(request):
    return render(request, "create-property.html", {
        "newpropertyform":NewPropertyForm(),
        "message":""
    })

def add_property(request):
    if request.method == "POST":
        form = NewPropertyForm(request.POST)
        if form.is_valid():
            try:
                extID = Property.objects.get(externalID=form.cleaned_data["externalID"])
            except:
                extID = None
            if extID:
                return render (request=request, template_name="create-property.html", context={"newpropertyform":form, "message":"A property with this externalID already exists."})
            extID = form.save()
            newprop = Property(externalID=form.cleaned_data["externalID"], city=form.cleaned_data["city"].capitalize(), latitude=form.cleaned_data["latitude"], longitude=form.cleaned_data["longitude"], rent=form.cleaned_data["rent"], areaSqm=form.cleaned_data["areaSqm"], isRoomActive=form.cleaned_data["isRoomActive"])
            newprop.save()
    form = NewPropertyForm()
    return render (request=request, template_name="create-property.html", context={"newpropertyform":form, "message":"Unable to create property."})

def retrieve_property(request):
    return render(request, "retrieve-property.html")

def extID_form(request):
    return render(request, 'extID-form.html')

def extID(request):
    if request.method == "POST":
        searched = request.POST["externalID"]
        properties = Data.objects.filter(externalID=searched)
        return render(request, 'property.html', {
            "properties":properties
        })

def lat_and_long_form(request):
    return render(request, 'lat-and-long-form.html')

def lat_and_long(request):
    if request.method == "POST":
        lat = request.POST["Latitude"]
        long = request.POST["Longitude"]
        properties = Data.objects.filter(latitude=lat, longitude=long)
        return render(request, 'property.html', {
            "properties":properties
        })

def budget_form(request):
    return render(request, 'budget-form.html')

def budget(request):
    if request.method == "POST":
        min = request.POST["Minimum"]
        max = request.POST["Maximum"]
        properties = Data.objects.filter(isRoomActive=True, rent__gte=min, rent__lte=max)
        return render(request, 'property.html', {
            "properties":properties
        })

def rent_form(request):
    return render(request, 'rent-form.html', {
        "rentform":NForm()
    })

def rent(request):
    if request.method == "POST":
        city = request.POST["city"]
        order = request.POST["order"]
        Num = request.POST["N"]
        if order == "Ascending":
            properties = Data.objects.filter(city=city).order_by('rent')[:Num]
        else:
            properties = Data.objects.filter(city=city).order_by('-rent')[:Num]
        return render(request, 'property.html', {
            "properties":properties
        })

def cost_per_sqm_form(request):
    return render(request, 'cost-per-sqm-form.html', {
        "costpersqmform":NForm()
    })

def cost_per_sqm(request):
    if request.method == "POST":
        city = request.POST["city"]
        order = request.POST["order"]
        Num = request.POST["N"]
        if order == "Ascending":
            properties = Data.objects.filter(city=city).order_by('costPerSqm')[:Num]
        else:
            properties = Data.objects.filter(city=city).order_by('-costPerSqm')[:Num]
        return render(request, 'property.html', {
            "properties":properties
        })

def update_property(request, id):
    property = Data.objects.filter(externalID=id)
    return render(request, "update-property.html", {
        "property":property
    })

def delete_property(request, id):
    property = Data.objects.filter(externalID=id)
    return render(request, "delete-property.html", {
        "property":property
    })

def confirm_delete_property(request, id):
    Data.objects.filter(externalID=id).delete()
    return render(request, "index.html")

def stats_city(request):
    if request.method == "POST":
        searched = request.POST["City"]
        properties = Data.objects.filter(city=searched)
        meanrent = Data.objects.filter(city=searched).aggregate(Avg('rent'))
        meandeposit = Data.objects.filter(city=searched).aggregate(Avg('deposit'))
        return render(request, "display_stats.html", {
            "searched":searched,
            "meanrent":meanrent,
            "meandeposit":meandeposit
        })

class NewPropertyForm(forms.Form):
    externalID = forms.CharField(label="externalID", required=True)
    city = forms.CharField(label="City")
    latitude = forms.FloatField(label="Latitude")
    longitude = forms.FloatField(label="Longitude")
    rent = forms.FloatField(label="Rent")
    areaSqm = forms.FloatField(label="Area in square meters")
    isRoomActive = forms.BooleanField(label="Is the room active for renting?", initial=False)

class NForm(forms.Form):
    city = forms.CharField(label="City", required=True)
    order = forms.Select(label="Order by", choices=["Ascending", "Descending"], required=True)
    N = forms.IntegerField(label="Number of properties to retrieve", min_value=1, initial=10)