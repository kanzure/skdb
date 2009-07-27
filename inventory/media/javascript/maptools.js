/*
  Deprecated, use map.js instead. ~~ SPM
*/

function mapinit() {
        map = new OpenLayers.Map ("map", {
                controls:[
                        new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.PanZoomBar(),
                        ],
                        maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
                        maxResolution: 156543.0399,
                        numZoomLevels: 17,
                        units: 'm',
                        projection: new OpenLayers.Projection("EPSG:900913"),
                        displayProjection: new OpenLayers.Projection("EPSG:4326")
                } );
 
        layerTilesAtHome = new OpenLayers.Layer.OSM.Osmarender("Osmarender");
        map.addLayer(layerTilesAtHome);
            
        layerTools = new OpenLayers.Layer.Markers("Tools");
    
        layerLabs = new OpenLayers.Layer.Markers("Labs");
        map.addLayer(layerLabs);
        layerLabs.events.on({
                'featureselected': onFeatureSelect,
                'featureunselected': onFeatureUnselect
        });

        var size = new OpenLayers.Size(21,25);
        var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
        var icon = new OpenLayers.Icon('http://www.openstreetmap.org/openlayers/img/marker.png',size,offset);
 
        if( ! map.getCenter() ){
                var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
                map.setCenter (lonLat, zoom);
        }

        return map;
}
        
function onPopupClose(evt) {
        // 'this' is the popup.
        selectControl.unselect(this.feature);
}
        
function onFeatureSelect(evt) {
        feature = evt.feature;
        popup = new OpenLayers.Popup.FramedCloud("featurePopup",
                        feature.geometry.getBounds().getCenterLonLat(),
                        new OpenLayers.Size(100,100),
                        'Foo!',
                        null, true, onPopupClose);
        feature.popup = popup;
        popup.feature = feature;
        map.addPopup(popup);
}

function onFeatureUnselect(evt) {
        feature = evt.feature;
        if (feature.popup) {
                popup.feature = null;
                map.removePopup(feature.popup);
                feature.popup.destroy();
                feature.popup = null;
        }
}

function createMarker(lat, lon, latdeg, latmin, latsec, latdir, londeg, lonmin, lonsec, londir, H, username, fullname, description, qthdescription, imagename, icon) {
        // new OpenLayers.Marker(lonLat,icon),
        var point = new OpenLayers.LonLat(lon, lat);
        var marker = new OpenLayers.Marker(point, icon);
        marker.attributes.H = H;
        marker.attributes.description = description;
        marker.attributes.qthdescription = qthdescription;
        marker.attributes.username = username;
        marker.attributes.fullname = fullname;
        marker.attributes.imagename = imagename;
        marker.attributes.lat = lat;
        marker.attributes.lon = lon;
        marker.attributes.latdeg = latdeg;
        marker.attributes.londeg = londeg;
        marker.attributes.latmin = latmin;
        marker.attributes.lonmin = lonmin;
        marker.attributes.latsec = latsec;
        marker.attributes.lonsec = lonsec;
        
        return marker;
}

function quickLocation(lat, lon, z) {
        map.setCenter(new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), z);
}
