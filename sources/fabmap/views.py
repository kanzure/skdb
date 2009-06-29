from django.shortcuts import render_to_response
from fabmap.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
	siteform = SiteForm()
	return render_to_response("fabmap/index.html", {"siteform": siteform, "user": request.user, "userauthed": request.user.is_authenticated()})

def search(request):
	# Handle search requests
	
	query = request.GET['q']
	if not query or query == "":
		sites = Site.objects.all()		
	else:
		sites = Site.objects.all()

	results = "{ 'sites': ["

	for site in sites:
		results += "{ 'lat': '%lf', 'lon': '%lf', 'name': '%s', 'locname': '%s', 'website': '%s'}" % (site.lat, site.lon, site.name, site.locname, site.website)
		# if sit:
		results += ","
		
	results += "]}"

	return HttpResponse(results)
	

def addsite(request):
	# Handle Add Site requests
	saved = False
	error = "Not handled"

	siteform = SiteForm(request.GET)
	if not request.user.is_authenticated():
		return HttpResponse("{'saved': '%d', 'error': '%s'}" % (saved, "You must be logged in to register sites."))
		
	if siteform.is_valid():
		site = siteform.save(commit=False)
		site.manager = request.user
		site.save()
		saved = True
		return HttpResponse("{'saved': '%d'}" % saved)
	else:
		error = "Must fill required fields."
		return HttpResponse("{'saved': '%d', 'error': '%s', 'newtable': '%s'}" % (saved, error, siteform.as_table().replace("\n","\\n")))

