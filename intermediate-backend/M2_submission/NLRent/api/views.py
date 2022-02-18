from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PropertySerializer
from .serializers import Property

import json

from statistics import mean, median, stdev

# Create your views here.



properties_list = []
with open('properties', 'r') as json_file:
	property_data = json.loads(json_file.read())
	for p in property_data:
		properties_list.append(Property(**p))

@api_view(['GET'])
def apiUrls(request):
	api_urls = {
		'Api Urls':'',
		'Search by externalId':'property/<externalId>/',
		'Search by Latitude and Longitude':'/property/<latitude>/<longitude>/',
		'Create Property':'create/',
		'Update Property by externalId':'update/<externalId>/',
		'Delete Property by externalId':'delete/<externalId>/',
		'Update Property by Latitude and Longitude':'update/<latitude>/<longitude>/',
		'Delete Property by Latitude and Longitude':'delete/<latitude>/<longitude>/',
		'Search by City':'city/<city>/',
		'Search by Budget':'budget/<city>/<minimum>/<maximum>/',
		'Top N Properties in a City by Rent':'top-rent/<city>/<order>/<N>/',
		'Top N Properties in a City by Cost Per Square Meter':'top-cost-per-sqm/<city>/<order>/<N>/',
		'Descriptive Statistics of Properties by City':'statistics/<city>/',
		}
	return Response(api_urls, status=200)

@api_view(['GET'])
def propertyDetail(request, pk):
	property = [x for x in properties_list if x.externalId == pk]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	serializer_list = []
	for p in property:
		serializer_list.append(p.toJSON())
	return Response(serializer_list)

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

@api_view(['POST'])
def propertyUpdate(request, pk):
	index = next((i for i, item in enumerate(properties_list) if item.externalId == pk), None)
	if index is None:
		return Response("Property with given externalId does not exist", status=204)
	property_object = Property(**request.data)
	if property_object.externalId != pk:
		return Response("Cannot change externalId of a property", status=409)
	properties_list[index] = property_object
	return Response(property_object.toJSON())

@api_view(['DELETE'])
def propertyDelete(request, pk):
	index = next((i for i, item in enumerate(properties_list) if item.externalId == pk), None)
	if index is None:
		return Response("Property with given externalId does not exist", status=204)
	properties_list.pop(index)
	return Response("Property deleted")

@api_view(['POST'])
def propertyUpdateLatLong(request, lat, long):
	index = next((i for i, item in enumerate(properties_list) if float(item.latitude) == float(lat) and float(item.longitude) == float(long)), None)
	if index is None:
		return Response("Property with given latitude and longitude does not exist", status=204)
	property_object = Property(**request.data)
	properties_list[index] = property_object
	return Response(property_object.toJSON())

@api_view(['DELETE'])
def propertyDeleteLatLong(request, lat, long):
	index = next((i for i, item in enumerate(properties_list) if float(item.latitude) == float(lat) and float(item.longitude) == float(long)), None)
	if index is None:
		return Response("Property with given latitude and longitude does not exist", status=204)
	properties_list.pop(index)
	return Response("Property deleted")

@api_view(['GET'])
def propertyByCity(request, city):
	property = [x for x in properties_list if x.city == city]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	serializer_list = []
	for p in property:
		serializer_list.append(p.toJSON())
	return Response(serializer_list)

@api_view(['GET'])
def propertyByLatLong(request, lat, long):
	property = [x for x in properties_list if float(x.latitude) == float(lat) and float(x.longitude) == float(long)]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	serializer_list = []
	for p in property:
		serializer_list.append(p.toJSON())
	return Response(serializer_list)

@api_view(['GET'])
def propertyByRent(request, city, min, max):
	property = [x for x in properties_list if x.city == city and int(x.rent) >= int(min) and int(x.rent) <= int(max) and x.isRoomActive == "true"]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	serializer_list = []
	for p in property:
		serializer_list.append(p.toJSON())
	return Response(serializer_list)

@api_view(['GET'])
def topNByRent(request, city, order, n):
	property = [x for x in properties_list if x.city == city and x.isRoomActive == "true"]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	if order == "descending":
		property.sort(key=lambda x: x.rent, reverse=True)
	elif order == "ascending":
		property.sort(key=lambda x: x.rent)
	else:
		return JsonResponse("Invalid Url: Order must be one of ascending/descending", safe=False)
	n = int(n)
	if n < 1:
		n = 10
	n = min(n, len(property))
	property = property[:n]
	serializer_list = []
	for p in property:
		serializer_list.append(p.toJSON())
	return Response(serializer_list)

@api_view(['GET'])
def topNByCostPerSqm(request, city, order, n):
	property = [x for x in properties_list if x.city == city and x.isRoomActive == "true"]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	if order == "descending":
		property.sort(key=lambda x: x.costPerSqm, reverse=True)
	elif order == "ascending":
		property.sort(key=lambda x: x.costPerSqm)
	else:
		return JsonResponse("Invalid Url: Order must be one of ascending/descending", safe=False)
	n = int(n)
	if n < 1:
		n = 10
	n = min(n, len(property))
	property = property[:n]
	serializer_list = []
	for p in property:
		serializer_list.append(p.toJSON())
	return Response(serializer_list)

@api_view(['GET'])
def stats(request, city):
	property = [x for x in properties_list if x.city == city and x.rent is not None and x.deposit is not None]
	if len(property) == 0:
		return Response("No properties match the given search", status=204)
	mean_cost = mean(p.rent for p in property)
	median_cost = median(p.rent for p in property)
	stdev_cost = stdev(p.rent for p in property)
	mean_deposit = mean(p.deposit for p in property)
	median_deposit = median(p.deposit for p in property)
	stdev_deposit = stdev(p.deposit for p in property)
	stats = {
		'Mean Rental Cost': mean_cost,
		'Median Rental Cost': median_cost,
		'Standard Deviation in Rental Cost': stdev_cost,
		'Mean Deposit': mean_deposit,
		'Median Deposit': median_deposit,
		'Standard Deviation in Deposit': stdev_deposit,
	}
	return Response(stats)