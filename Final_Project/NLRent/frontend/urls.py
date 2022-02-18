from django.urls import path, re_path
from . import views

urlpatterns = [
	path("", views.index),
	re_path(r"update-property-[\w]+-[0-9]{1,}$", views.updateProperty),
	re_path(r"delete-property-[\w]+-[0-9]{1,}$", views.deleteProperty),
	path("create-property", views.createProperty),
	path("search-properties", views.searchProperties),
]
