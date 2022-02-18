from rest_framework import serializers
# from .views import Property
import json

class Property:
	def __init__(self, externalId, city=0, latitude=0, longitude=0, rent=None, areaSqm=None, isRoomActive="false", deposit=None,
	_id=0, areaRaw=0, coverImageUrl=0, crawlStatus=0, crawledAt=0, datesPublished=0, firstSeenAt=0, furnish=0, lastSeenAt=0, postalCode=0, postedAgo=0, propertyType=0, rawAvailability=0, rentDetail=0, rentRaw=0, source=0, title=0, url=0, additionalCosts=0, additionalCostsRaw=0, depositRaw=0, descriptionNonTranslated=0, descriptionNonTranslatedRaw=0, descriptionTranslated=0, descriptionTranslatedRaw=0, detailsCrawledAt=0, energyLabel=0, gender=0, internet=0, kitchen=0, living=0, matchAge=0, matchAgeBackup=0, matchCapacity=0, matchGender=0, matchGenderBackup=0, matchLanguages=0, matchStatus=0, matchStatusBackup=0, pageDescription=0, pageTitle=0, pets=0, registrationCost=0, registrationCostRaw=0, roommates=0, shower=0, smokingInside=0, toilet=0, userDisplayName=0, userId=0, userLastLoggedOn=0, userMemberSince=0, userPhotoUrl=0, additionalCostsDescription=0
	):
		self.externalId = externalId
		self.city = city.capitalize()
		self.latitude = latitude
		self.longitude = longitude
		self.rent = rent
		self.areaSqm = areaSqm
		self.isRoomActive = isRoomActive
		self.deposit = deposit
		if rent is not None and areaSqm is not None:
			self.costPerSqm = rent / areaSqm
		else:
			self.costPerSqm = None
		self.costPerSqm = round(self.costPerSqm, 4)
	
	def patch(self, externalId=0, city=None, latitude=None, longitude=None, rent=None, areaSqm=None, isRoomActive=None, deposit=None):
		if city is not None:
			self.city = city
		if latitude is not None:
			self.latitude = latitude
		if longitude is not None:
			self.longitude = longitude
		if rent is not None:
			self.rent = rent
		if areaSqm is not None:
			self.areaSqm = areaSqm
		if isRoomActive is not None:
			self.isRoomActive = isRoomActive
		if deposit is not None:
			self.deposit = deposit

	@classmethod
	def from_json(cls, json_string):
		json_dict = json.loads(json_string)
		return cls(**json_dict)
	
	def toJSON(self):
		return json.loads(json.dumps(self, default=lambda o: o.__dict__))
	
	def toCSV(self, tag=0):
		if tag == 1:
			ret = "externalId, city, latitude, longitude, rent, areaSqm, isRoomActive, deposit, costPerSqm\n"
		else:
			ret = ""
		ret += str(self.externalId)
		ret += ", "
		ret += self.city
		ret += ", "
		ret += str(self.latitude)
		ret += ", "
		ret += str(self.longitude)
		ret += ", "
		ret += str(self.rent)
		ret += ", "
		ret += str(self.areaSqm)
		ret += ", "
		ret += str(self.isRoomActive)
		ret += ", "
		ret += str(self.deposit)
		ret += ", "
		ret += str(self.costPerSqm)
		ret += '\n'
		return ret

	def __repr__(self):
		return f'Property {self.externalId}'

class PropertySerializer(serializers.ModelSerializer):
	class Meta:
		model = Property
		fields = ('externalId', 'city', 'latitude', 'longitude', 'rent', 'areaSqm', 'isRoomActive', 'costPerSqm', 'deposit')
		
