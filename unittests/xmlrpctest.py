#
#  XMLRPC interface test
#
#

import xmlrpclib

server = xmlrpclib.Server("http://127.0.0.1:8000/xmlrpc/")

for site in server.FabMapGetSites():
	print "Name: %s\nLocation: %s\nLongitude: %lf\nLatitude: %lf\nWebsite: %s" % (site['name'], site['locname'], site['lon'], site['lat'], site['website'])
	details = server.FabMapGetSiteDetails(site['id'])
	print details
	print "-----------------------"
