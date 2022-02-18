from django.db import models

# Create your models here.
class Property(models.Model):
    externalID = models.CharField(primary_key=True, null=False, unique=True, max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rent = models.FloatField()
    areaSqm = models.FloatField()
    isRoomActive = models.BooleanField(default=False)
    costPerSqm = models.FloatField()

