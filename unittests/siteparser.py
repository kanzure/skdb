import libxml2

fh = open("sitetest.xml")
input = libxml2.inputBuffer(fh)
reader = input.newTextReader("")

sites = {}
reader.Read()

siteID = ""

while reader.Read():
        if reader.Name() == "site":
                siteID = reader.GetAttribute("id")
                sites[siteID] = {}
        
        if reader.Name() in ("datetime", "name", "locname", "latitude", "longitude", "website", "access"):
                print "found " + reader.Name() + " node"
                sites[siteID][reader.Name()] = reader.ReadInnerXml()
                
print sites
                