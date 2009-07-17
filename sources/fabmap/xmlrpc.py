from fabmap.models import *

def getsitelist():
	"""Returns a list of sites."""

	sites = Site.objects.all()		

	results = []

	for site in sites:
		results.append({ 'id': site.id, 'lat': site.lat, 'lon': site.lon, 'name': site.name, 'locname': site.locname, 'website': site.website})

	return results

def getsitedetails(siteid):
	site = Site.objects.get(id=siteid)
	if site.id:
		vals = {"site": site}
		equipcnt = site.equipment_set.count()
		if equipcnt > 0:
			equip = []
			for equipment in site.equipment_set.iterator():
				caps = []
				for capability in equipment.type.capabilities.iterator():
					caps.append(capability.name)
				equip.append({"type": equipment.type.name, "maker": equipment.type.maker, "capabilities": caps, "notes": equipment.notes})
			vals['equipment'] = equip
		
		return vals
	else:
		return {}

def getequipmenttypes():
	return {}


