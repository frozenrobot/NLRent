from django.urls import path
from . import views

urlpatterns = [
	path("", views.apiUrls, name="index"),
	path("property/<str:pk>/", views.propertyDetail, name="byExternalId"),
	path("create/", views.propertyCreate, name="create"),
	path("update/<str:pk>/", views.propertyUpdate, name="update"),
	path("delete/<str:pk>/", views.propertyDelete, name="delete"),
	path("update/<lat>/<long>/", views.propertyUpdateLatLong, name="updateLatLong"),
	path("delete/<lat>/<long>/", views.propertyDeleteLatLong, name="deleteLatLong"),
	path("city/<str:city>/", views.propertyByCity, name="byCity"),
	path("property/<lat>/<long>/", views.propertyByLatLong, name="byLatLong"),
	path("budget/<city>/<min>/<max>/", views.propertyByRent, name="byRent"),
	path("top-rent/<city>/<order>/<n>/", views.topNByRent, name="topByRent"),
	path("top-cost-per-sqm/<city>/<order>/<n>/", views.topNByCostPerSqm, name="topByCostPerSqm"),
	path("statistics/<city>/", views.stats, name="stats")
]