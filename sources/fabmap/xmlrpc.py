from fabmap.models import *

# TODO: Authentication!!!
# TODO: Better error handling

def GetSiteList():
	"""Returns a list of sites."""

	sites = Site.objects.all()		

	results = []

	for site in sites:
		results.append({ 'id': site.id, 'lat': site.lat, 'lon': site.lon, 'name': site.name, 'locname': site.locname, 'website': site.website})

	return results

def GetSiteDetails(siteid):
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

def GetEquipmentTypes():
	equiptypes = EquipmentType.objects.all()
	
	results = []
	for e in equiptypes.iterator:
		caps = []
		for capability in e.capabilities.iterator():
			caps.append(capability.name)
		results.append({'name': e.name, 'maker': e.maker, 'capabilities': caps})
	
	return results
	
def GetCapabilities():
	caps = EquipmentCapability.objects.all()
	ret = []
	for a in caps.iterator():
		ret.append({'id': a.id, 'name': a.name})
	return ret
	
def AddEquipmentType(name, maker, capabilities):
	# Register an equipment type
	et = EquipmentType(name=name, maker=maker)
	et.save()
	for a in capabilities:
		if type(a) is int:
			et.capabilities.add(a)
	et.save()
	return {'saved': True}
	
def AddEquipment(siteid, equipmenttype, notes):
	# Register equipment
	eq = Equipment(type=equipmenttype, site=siteid, notes=notes)
	eq.save()
	return {'saved': True}

def AddSite(name, locname, lat, lon, website, access):
	# Add a site.
	manager = 1
	# FIXME: Here we should make manager be the same as the authed user.
	site = Site(name=name, locname=locname, lat=lat, lon=lon, website=website, manager=manager, access=access)
	site.save()
	return {'saved': True}
	
def AddCapability(capability):
	# Add a capability class
	cap = EquipmentCapability(name=capability)
	cap.save()
	return {'saved': True, 'id': cap.id}
	
def FindEquipmentByCapability(capid):
	# Return a list of equipment, and each equipment type contains a list of sites where it exists.
	
	return {}

