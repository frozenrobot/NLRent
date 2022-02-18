from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("create-property", views.create_property, name="create_property"),
	path("retrieve-property", views.retrieve_property, name="retrieve_property"),
	path("update-property", views.update_property, name="update_property"),
	path("delete-property", views.delete_property, name="delete_property"),
	#path("descriptive-statistics", views.compute_stats, name="compute_stats"),
]