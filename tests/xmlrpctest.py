#
#  XMLRPC interface test
#
#

import xmlrpclib

server = xmlrpclib.Server("http://127.0.0.1:8000/xmlrpc/")

print server.GetCapabilities()

for site in server.GetSites():
        print "Name: %s\nLocation: %s\nLongitude: %lf\nLatitude: %lf\nWebsite: %s" % (site['name'], site['locname'], site['lon'], site['lat'], site['website'])
        details = server.GetSiteDetails(site['id'])
        print details
        print "-----------------------"

