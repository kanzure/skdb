import settings
from django.shortcuts import render_to_response
from fabmap.models import *
from fabmap.xmlrpc import *
from django.http import HttpResponse
from django.contrib.auth.models import User
import simplejson

def index(request):
	addsiteform = SiteForm(auto_id="addsite_")
	editsiteform = SiteForm(auto_id="editsite_")
	return render_to_response("fabmap/index.html", {"addsiteform": addsiteform, "editsiteform": editsiteform, "user": request.user, "userauthed": request.user.is_authenticated()})

def search(request):
	# Handle search requests
	
	query = request.GET['q']
	if not query or query == "":
		return HttpResonse(simplejson.encode(GetSiteList()))
	else:
		# FIXME: This isn't actually a real search function at the moment.
		return HttpResonse(simplejson.encode(GetSiteList()))

def setsite(request):
	if not request.has_key('siteid'):
		return HttpResponse(simplejson.encode({'error': 'Must supply site ID'}))
	
	siteid = request.GET['siteid']
	vars = {}
	for a in ('name', 'locname', 'latitude', 'longitude', 'website', 'access'):
		if request.GET.has_key(a):
			vars[a] = request.GET[a]
		else:
			vars[a] = None
			
	SetSite(siteid, **vars)

def getsite(request):
	if not request.GET['siteid']:
		return HttpResponse(simplejson.encode({'error': 'Must supply site ID'}))
	return HttpResponse(simplejson.encode(GetSiteDetails(request.GET['siteid'])))

def addsite(request):
	# Handle Add Site requests
	response = {'saved': False, 'error': "Not handled"}

	siteform = SiteForm(request.GET)
	
	if not request.user.is_authenticated():
		response["error"] = "You must be logged in to register sites."
		return HttpResponse(simplejson.encode(response))
		
	if siteform.is_valid():
		site = siteform.save(commit=False)
		site.manager = request.user
		site.save()
		response["saved"] = True
		return HttpResponse(simplejson.encode(response))
	else:
		response["error"] = "Must fill required fields."
		response["newtable"] = siteform.as_table()
		return HttpResponse(simplejson.encode(response))

def sitedetails(request):
	# Return very detailed information about a site.
	if not request.GET.has_key('siteid'):
		return HttpResponse(simplejson.encode({'error': 'Must supply ID'}))
	
	return HttpResponse(simplejson.encode(GetSiteDetails(request.GET['siteid'])))
	

def addequipment(request):
	return HttpResponse("")
	
def addequipmenttype(request):
	return HttpResponse("")
	
	
