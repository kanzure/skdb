/*
 *   Site management
 * 
 *      by Smári McCarthy
 *
 *      Freely distributable under the terms of the GNU General Public License v3.0
 */

function Site() {
        var siteid;
        var latitude;
        var longitude;
        var name;
        var locname;
        var website;
        var access;
        var equipment;
        
        return {
                GetSite: function(siteid) {
                        $.getJSON("/dmed/getsite", {'siteid': siteid}, this.ReadSite());
                },
                
                ReadSite: function(data, s) {
                        if (data['error']) {
                                // Handle error!
                        }
                        siteid = data['site']['id'];
                        latitude = data['site']['latitude'];
                        longitude = data['site']['longitude'];
                        name = data['site']['name'];
                        locname = data['site']['locname'];
                        website = data['site']['website'];
                        access = data['site']['access'];
                        equipment = data['equipment'];
                },
                
                SetSite: function() {
                        $.getJSON("/dmed/setsite", {'siteid': siteid, 'name': pname, 'locname': ploc, 'latitude': latitude, 'longitude': longitude, 'website': pwww, 'access': pacc}, this.ReadSite());
                },
                
                AddSite: function(pname, ploc, plat, plon, pwww, pacc) {
                        $.getJSON("/dmed/addsite", {'name': pname, 'locname': ploc, 'latitude': latitude, 'longitude': longitude, 'website': pwww, 'access': pacc}, this.ReadSite());
                },
                
                SetLocation: function(pname) {
                        locname = pname;
                        this.SetSite();
                },
                
                SetLatLon: function(plat, plon) {
                        latitude = plat;
                        longitude = plon;
                        this.SetSite();
                },
                
                SetName: function(pname) {
                        name = pname;
                        this.SetSite();
                },
                
                SetWebsite: function(www) {
                        website = www;
                        this.SetSite();
                },
                
                AddEquipment: function(typeid) {
                        $.getJSON("/dmed/addequipment", {'siteid': siteid, 'type': typeid}, this.ReadSite());
                },
                
        };
}


function SiteManager() {
        var site;
        var sitedialog;
        var sitewidgets = {};
        
}


function newSite() {
        hideDialog($('#addSiteDialog'));
        showProgress('Saving...');
        $.getJSON("/dmed/addsite", 
                {'lat': $('#addsite_lat').val(),
                'lon': $('#addsite_lon').val(),
                'name': $('#addsite_name').val(),
                'locname': $('#addsite_locname').val(),
                'website': $('#addsite_website').val(),
                'access': $('#addsite_access').val() },
                function(data, s) {
                        hideProgress();
                        if (data['newtable']) {
                                $('#addsiteform').html(data['newtable']);
                                showDialog($('#addSiteDialog'));
                        } else {
                                if (data['saved'] == 0) {
                                        showStatus('Save failed: ' + data['error'], 5000)
                                } else {
                                        showStatus('Saved');
                                }
                        }
                });
}

function editLoc(id) {
        showProgress();
        $.getJSON("/dmed/sitedetails", {'id': id}, function(data, s) {
                hideProgress();
                showDialog($('#editSiteDialog'));
        });
}

function addSearchResult(id, lat, lon, name, loc, website) {
        str = "<tr>";
        str += "<td>" + name + "</td><td>" + loc + "</td>";
        /* {%if userauthed%}str+= "<td><a href=\"#\" onclick=\"editLoc(" + id + ");\">Edit</a></td>";{%endif%} */
        str += "</tr>";
        $('#searchresults_table').append(str);
}

function search(q) {
        if (q == undefined) {
                q = $('#q').val();
        }
        $('#searchresults_table').empty().append("<tr><th>Site name</th><th>Location</th></tr>");
        $.getJSON("/dmed/search", {'q': q}, function(data, s) {
                for (var i = 0; i < data['sites'].length; i++) {
                        a = data['sites'][i];
                        map.quickMarker("sites", a['lat'], a['lon'], a['name'], a['locname'], a['website']);
                        addSearchResult(a['id'], a['lat'], a['lon'], a['name'], a['locname'], a['website']);
                }
        });
}

function handleClick(e) {
        var lonlat = map.getLonLatFromViewPortPx(e.xy);
        alert("You clicked near " + lonlat.lat + " N, " +
                      + lonlat.lon + " E");
}

