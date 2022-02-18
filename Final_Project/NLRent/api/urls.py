from django.urls import path
from . import views

urlpatterns = [
	path("", views.apiUrls, name="index"),
	path("property/", views.propertyCreate, name="create"),
	path("property/<str:pk>/", views.property, name="property"),
	path('properties/', views.propertyLatLong, name="LatLong"),
	path("properties/city/", views.propertyByCity, name="byCity"),
	path("properties/budget/", views.propertyByRent, name="byRent"),
	path("properties/top-rent/", views.topByRent, name="topByRent"),
	path("properties/top-cost-per-sqm/", views.topByCostPerSqm, name="topByCostPerSqm"),
	path("statistics/", views.stats, name="stats"),
	path("properties/extra/", views.extra, name="extra"),
]
