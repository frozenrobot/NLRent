from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PropertySerializer
from .serializers import Property

import json
import requests

from statistics import mean, median, stdev

from django.conf import settings

import pandas as pd

# Create your views here.
properties_list = []
with open('properties', 'r') as json_file:
	property_data = json.loads(json_file.read())
	for p in property_data:
		properties_list.append(Property(**p))

@api_view(['GET'])
def apiUrls(request):
	api_urls = {
		'Api Urls':'api/',
		'Create Property':'api/property/',
		'Get, Update or Delete Property by externalId':'api/property/<externalId>/',
		'Get, Update or Delete Property by Latitude and Longitude':'api/properties/?lat=...&long=...',
		'Extra Information by Latitude and Longitude':'api/properties/extra/?lat=...&long=...',
		'Find all Properties in a City':'api/properties/city/?city=...',
		'Find all Properties in a City within a Budget':'api/properties/budget/?city=...&min=...&max=...',
		'Top N Properties in a City by Rent':'api/properties/top-rent/?city=...&order=...&n=...',
		'Top N Properties in a City by Cost Per Square Meter':'api/properties/top-cost-per-sqm/?city=...&order=...&n=...',
		'Descriptive Statistics of Properties by City':'api/statistics/?city=...',
	}
	return Response(api_urls, status=200)

@api_view(['GET'])
def extra(request):
	lat=request.GET.get('lat')
	long=request.GET.get('long')
	if lat and long:
		lat = float(lat)
		long = float(long)
	else:
		return JsonResponse("required query parameters: lat, long", status=400, safe=False)
	result = requests.get(
		'https://api.bigdatacloud.net/data/reverse-geocode-client/',
		params={
		'latitude': lat,
		'longitude': long,
		})
	csv = request.GET.get('csv')
	if result:
		results_json = result.json()
		pluscode = results_json["plusCode"]
		pr_subdiv = results_json["principalSubdivision"]
		pr_subdiv_code = results_json["principalSubdivisionCode"]
		locality = results_json["locality"]
		if csv and csv.lower() == "true":
			ret = "plusCode, principalSubdivision, principalSubdivisionCode, locality\n"
			ret += pluscode
			ret += ", "
			ret += pr_subdiv
			ret += ", "
			ret += pr_subdiv_code
			ret += ", "
			ret += locality
			ret += '\n'
			return HttpResponse(ret, content_type="text/csv")
		else:
			ret = {
				"plusCode":pluscode,
				"principalSubdivision":pr_subdiv,
				"principalSubdivisionCode":pr_subdiv_code,
				"locality":locality
			}
			return Response(ret, status=200)
	else:
		if csv and csv.lower() == "true":
			return HttpResponse("Not found", content_type="text/csv")
		else:
			ret = {
				"Result":"Not found"
			}
			return Response(ret, status=204)

@api_view(['GET', 'PATCH', 'DELETE'])
def property(request, pk):
	if(request.method == 'GET'):
		property = [x for x in properties_list if x.externalId.replace("%20", " ") == pk]
		if len(property) == 0:
			return Response("No properties match the given search", status=204)
		serializer_list = []
		csv = request.GET.get('csv')
		if csv and csv.lower() == "true":
			for p in property:
				serializer_list.append(p.toCSV(1))
			return HttpResponse(serializer_list, content_type="text/csv")
		else:
			for p in property:
				serializer_list.append(p.toJSON())
			return Response(serializer_list)
	if(request.method == 'PATCH'):
		index = next((i for i, item in enumerate(properties_list) if item.externalId == pk), None)
		if index is None:
			return Response("Property with given externalId does not exist", status=204)
		properties_list[index].patch(**request.data)
		if properties_list[index].rent is not None and properties_list[index].areaSqm is not None:
			properties_list[index].costPerSqm = properties_list[index].rent / properties_list[index].areaSqm
		else:
			properties_list[index].costPerSqm = None
		properties_list[index].costPerSqm = round(properties_list[index].costPerSqm, 4)
		return Response(properties_list[index].toJSON())
	if(request.method == 'DELETE'):
		index = next((i for i, item in enumerate(properties_list) if item.externalId == pk), None)
		if index is None:
			return Response("Property with given externalId does not exist", status=204)
		properties_list.pop(index)
		return Response("Property deleted")

@api_view(['POST'])
def propertyCreate(request):
	property_object = Property(**request.data)
	already_property = [x for x in properties_list if x.externalId == property_object.externalId]
	if already_property:
		return Response("Property with same externalId already exists", status=409)
	properties_list.append(property_object)
	serializer_list = []
	serializer_list.append(property_object.toJSON())
	return Response(serializer_list, status=201)

@api_view(['GET'])
def propertyByCity(request):
	city=request.GET.get('city')
	if city:
		city = city.capitalize()
	else:
		return JsonResponse("required query parameters: city", status=400, safe=False)
	property = [x for x in properties_list if x.city == city]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	serializer_list = []
	csv = request.GET.get('csv')
	if csv and csv.lower() == "true":
		ret = "externalId, city, latitude, longitude, rent, areaSqm, isRoomActive, deposit, costPerSqm\n"
		serializer_list.append(ret)
		for p in property:
			serializer_list.append(p.toCSV())
		return HttpResponse(serializer_list, content_type="text/csv")
	else:
		for p in property:
			serializer_list.append(p.toJSON())
		return Response(serializer_list)

@api_view(['GET', 'PATCH', 'DELETE'])
def propertyLatLong(request):
	lat=request.GET.get('lat')
	long=request.GET.get('long')
	if lat and long:
		lat = float(lat)
		long = float(long)
	else:
		return JsonResponse("required query parameters: lat, long", status=400, safe=False)
	if(request.method == 'GET'):
		property = [x for x in properties_list if float(x.latitude) == float(lat) and float(x.longitude) == float(long)]
		if len(property) == 0:
			return Response("No properties match the given search", status=204)
		serializer_list = []
		csv = request.GET.get('csv')
		if csv and csv.lower() == "true":
			ret = "externalId, city, latitude, longitude, rent, areaSqm, isRoomActive, deposit, costPerSqm\n"
			serializer_list.append(ret)
			for p in property:
				serializer_list.append(p.toCSV())
			return HttpResponse(serializer_list, content_type="text/csv")
		else:
			for p in property:
				serializer_list.append(p.toJSON())
			return Response(serializer_list)
	if(request.method == 'PATCH'):
		index = [i for i, item in enumerate(properties_list) if float(item.latitude) == float(lat) and float(item.longitude) == float(long)]
		if len(index) == 0:
			return Response("No properties with given latitude and longitude", status=204)
		for i in index:
			properties_list[i].patch(**request.data)
		serializer_list = []
		for i in index:
			serializer_list.append(properties_list[i].toJSON())
		return Response(serializer_list)
	if(request.method == 'DELETE'):
		index = [i for i, item in enumerate(properties_list) if float(item.latitude) == float(lat) and float(item.longitude) == float(long)]
		if len(index) == 0:
			return Response("No properties with given latitude and longitude", status=204)
		for i in reversed(index):
			properties_list.pop(i)
		return Response("Properties deleted")

@api_view(['GET'])
def propertyByRent(request):
	city=request.GET.get('city')
	min=request.GET.get('min')
	max=request.GET.get('max')
	if min and max and city:
		min = int(min)
		max = int(max)
		city = city.capitalize()
	else:
		return JsonResponse("required query parameters: city, min, max", status=400, safe=False)
	property = [x for x in properties_list if x.city == city and int(x.rent) >= int(min) and int(x.rent) <= int(max) and x.isRoomActive == "true"]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	serializer_list = []
	csv = request.GET.get('csv')
	if csv and csv.lower() == "true":
		ret = "externalId, city, latitude, longitude, rent, areaSqm, isRoomActive, deposit, costPerSqm\n"
		serializer_list.append(ret)
		for p in property:
			serializer_list.append(p.toCSV())
		return HttpResponse(serializer_list, content_type="text/csv")
	else:
		for p in property:
			serializer_list.append(p.toJSON())
		return Response(serializer_list)

@api_view(['GET'])
def topByRent(request):
	city=request.GET.get('city')
	order=request.GET.get('order')
	if city and order:
		city = city.capitalize()
		order = order.lower()
	else:
		return JsonResponse("required query parameters: city, order", status=400, safe=False)
	n=request.GET.get('n')
	if n is not None:
		n = int(n)
		if (n < 1):
			n = 10
	else:
		n = 10
	property = [x for x in properties_list if x.city == city and x.isRoomActive == "true"]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	if order == "descending":
		property.sort(key=lambda x: x.rent, reverse=True)
	elif order == "ascending":
		property.sort(key=lambda x: x.rent)
	else:
		return JsonResponse("Invalid Url: Order must be one of ascending/descending", safe=False)
	n = min(n, len(property))
	property = property[:n]
	serializer_list = []
	csv = request.GET.get('csv')
	if csv and csv.lower() == "true":
		ret = "externalId, city, latitude, longitude, rent, areaSqm, isRoomActive, deposit, costPerSqm\n"
		serializer_list.append(ret)
		for p in property:
			serializer_list.append(p.toCSV())
		return HttpResponse(serializer_list, content_type="text/csv")
	else:
		for p in property:
			serializer_list.append(p.toJSON())
		return Response(serializer_list)

@api_view(['GET'])
def topByCostPerSqm(request):
	city=request.GET.get('city')
	order=request.GET.get('order')
	if city and order:
		city = city.capitalize()
		order = order.lower()
	else:
		return JsonResponse("required query parameters: city, order", status=400, safe=False)
	n=request.GET.get('n')
	if n is not None:
		n = int(n)
		if (n < 1):
			n = 10
	else:
		n = 10
	property = [x for x in properties_list if x.city == city and x.isRoomActive == "true"]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	if order == "descending":
		property.sort(key=lambda x: x.costPerSqm, reverse=True)
	elif order == "ascending":
		property.sort(key=lambda x: x.costPerSqm)
	else:
		return JsonResponse("Invalid Url: Order must be one of ascending/descending", safe=False)
	n = min(n, len(property))
	property = property[:n]
	serializer_list = []
	csv = request.GET.get('csv')
	if csv and csv.lower() == "true":
		ret = "externalId, city, latitude, longitude, rent, areaSqm, isRoomActive, deposit, costPerSqm\n"
		serializer_list.append(ret)
		for p in property:
			serializer_list.append(p.toCSV())
		return HttpResponse(serializer_list, content_type="text/csv")
	else:
		for p in property:
			serializer_list.append(p.toJSON())
		return Response(serializer_list)

@api_view(['GET'])
def stats(request):
	city=request.GET.get('city')
	if city is not None:
		city = city.capitalize()
	else:
		return JsonResponse("required query parameters: city", status=400, safe=False)
	property = [x for x in properties_list if x.city == city and x.rent is not None and x.deposit is not None]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	mean_cost = mean(p.rent for p in property)
	median_cost = median(p.rent for p in property)
	stdev_cost = stdev(p.rent for p in property)
	mean_deposit = mean(p.deposit for p in property)
	median_deposit = median(p.deposit for p in property)
	stdev_deposit = stdev(p.deposit for p in property)
	csv = request.GET.get('csv')
	if csv and csv.lower() == "true":
		ret = "Mean Rental Cost, Median Rental Cost, Standard Deviation in Rental Cost, Mean Deposit, Median Deposit, Standard Deviation in Deposit\n"
		ret += str(mean_cost)
		ret += ", "
		ret += str(median_cost)
		ret += ", "
		ret += str(stdev_cost)
		ret += ", "
		ret += str(mean_deposit)
		ret += ", "
		ret += str(median_deposit)
		ret += ", "
		ret += str(stdev_deposit)
		ret += '\n'
		return HttpResponse(ret, content_type="text/csv")
	else: 
		stats = {
			'Mean Rental Cost': mean_cost,
			'Median Rental Cost': median_cost,
			'Standard Deviation in Rental Cost': stdev_cost,
			'Mean Deposit': mean_deposit,
			'Median Deposit': median_deposit,
			'Standard Deviation in Deposit': stdev_deposit,
		}
		return Response(stats)
