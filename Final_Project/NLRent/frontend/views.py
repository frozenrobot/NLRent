from django.shortcuts import render

def index(request):
	return render(request, 'frontend/index.html')

def createProperty(request):
	return render(request, 'frontend/index.html')
	
def updateProperty(request):
	return render(request, 'frontend/index.html')
	
def deleteProperty(request):
	return render(request, 'frontend/index.html')
	
def searchProperties(request):
	return render(request, 'frontend/index.html')
