import settings
from django.shortcuts import render_to_response
from fabmap.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
	addsiteform = SiteForm(auto_id="addsite_")
	editsiteform = SiteForm(auto_id="editsite_")
	return render_to_response("fabmap/index.html", {"addsiteform": addsiteform, "editsiteform": editsiteform, "user": request.user, "userauthed": request.user.is_authenticated()})

def search(request):
	# Handle search requests
	
	query = request.GET['q']
	if not query or query == "":
		sites = Site.objects.all()		
	else:
		# FIXME: This isn't actually a real search function at the moment.
		sites = Site.objects.all()

	results = "{ 'sites': ["

	for site in sites:
		results += "{ 'id': '%d', 'lat': '%lf', 'lon': '%lf', 'name': '%s', 'locname': '%s', 'website': '%s'}," % (site.id, site.lat, site.lon, site.name, site.locname, site.website)
		
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

def sitedetails(request):
	# Return very detailed information about a site.
	if not request.GET.has_key('id'):
		return HttpResponse("{'error': 'Must supply ID'}")
	
	site = Site.objects.get(id=request.GET['id'])
	if site.id:
		return render_to_response("fabmap/sitedetails.json", {"site": site, "equipment": site.equipment_set.all()})
	else:
		HttpResponse("{'error': 'ID not found'}")
	

def addequipment(request):
	return HttpResponse("")
	
def addequipmenttype(request):
	return HttpResponse("")
	
	
