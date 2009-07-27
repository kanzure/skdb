/*
 *   Map - Easy to use OpenLayers map object
 * 
 *      by Smári McCarthy & Olle Jonsson
 *
 *      Freely distributable under the terms of the GNU General Public License v3.0
 */

function Map() {
        var map;
        var layers = {};
        var icon;
        
        return {
        
                getMap: function() {
                        return map;
                },
        
                init: function(element, mlat, mlon, mzoom) {

                        // Where to focus at first
                        var lat=23;
                        var lon=0;
                        var zoom=2;
                        if (mlat != undefined) {
                                var lat = mlat;
                        }
                        if (mlon != undefined) {
                                var lon = mlon;
                        }
                        if (mzoom != undefined) {
                                var zoom = mzoom;
                        }

                        // Create the map itself...
                        map = new OpenLayers.Map(element, {
                                controls:[
                                        new OpenLayers.Control.Navigation(),
                                        new OpenLayers.Control.PanZoomBar(),
                                        new OpenLayers.Control.MousePosition(),
                                        new OpenLayers.Control.LayerSwitcher(),
                                ],
                                maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
                                maxResolution: 156543.0399,
                                numZoomLevels: 17,
                                units: 'm',
                                projection: new OpenLayers.Projection("EPSG:900913"),
                                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                                // I don't know why we're registering all these event listeners? Can't we do this a smarter way?
                                eventListeners: {
                                        "moveend": this.onMapEvent,
                                        "zoomend": this.onMapEvent,
                                        "changelayer": this.onMapLayerChanged,
                                        "changebaselayer": this.onMapBaseLayerChanged,
                                }
                        } );
 
                        // FIXME: We want to be able to control arbitrary layers here. for more general purpose mapping
 
                        // The TilesAtHome layer...
                        layers["mapnik"] = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
                        layers["tilesathome"] = new OpenLayers.Layer.OSM.Osmarender("Tiles@Home");
                        map.addLayers([layers["tilesathome"], layers["mapnik"]]);
                        
                        // The Sites layer...
                        layers["sites"] = new OpenLayers.Layer.Markers("Sites");
                        map.addLayer(layers["sites"]);
                        
                        layers["sites"].events.on({
                                'featureselected': this.onFeatureSelect,
                                'featureunselected': this.onFeatureUnselect
                        });
         
                        // Zoom to the initial center
                        if( ! map.getCenter() ){
                                var lonLat = new OpenLayers.LonLat(lon, lat).transform(map.displayProjection, map.projection);
                                map.setCenter (lonLat, zoom);
                        }
                        
                        // Return the map object for handy direct manipulation.
                        return map;
                },
                
                onMapEvent: function(evt) {
                
                },
                
                onMapLayerChanged: function(evt) {
                
                },
                
                onMapBaseLayerChanged: function(evt) {
                
                },
        
                onFeatureSelect: function(evt) {
                        var feature = evt.feature;
                        var popup = new OpenLayers.Popup.FramedCloud("featurePopup",
                                feature.geometry.getBounds().getCenterLonLat(),
                                new OpenLayers.Size(100,100),
                                'Foo!',
                                null, true, this.onPopupClose);
                        feature.popup = popup;
                        popup.feature = feature;
                        map.addPopup(popup);
                },
                
                onFeatureUnselect: function (evt) {
                        var feature = evt.feature;
                        if (feature.popup) {
                                popup.feature = null;
                                map.removePopup(feature.popup);
                                feature.popup.destroy();
                                feature.popup = null;
                        }
                },
        
                createMarker: function(lat, lon, name, locname, website) {
                        // new OpenLayers.Marker(lonLat,icon),
                        // Create a handy marker icon... (FIXME: this should be elsewhere)
                        var size = new OpenLayers.Size(21,25);
                        var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
                        var icon = new OpenLayers.Icon('http://www.openstreetmap.org/openlayers/img/marker.png',size,offset);
                        var point = new OpenLayers.LonLat(lon, lat).transform(map.displayProjection, map.projection);
                        var marker = new OpenLayers.Marker(point, icon);
                        // var m = marker.attributes;
                        // m.lat = lat;
                        // m.lon = lon;
                        // m.name = name;
                        // m.locname = locname;
                        // m.website = website;
                        return marker;
                },
                
                addMarker: function(layer, marker) {
                        if (layers[layer] != undefined) {
                                layers[layer].addMarker(marker);
                        }
                },
                
                // FIXME: This needs generalizing
                quickMarker: function(layer, lat, lon, name, locname, website, icon) {
                        this.addMarker(layer, this.createMarker(lat, lon, name, locname, website));
                },
        
                zoomLocation: function(lat, lon, zoom) {
                        map.setCenter(new OpenLayers.LonLat(lon, lat).transform(map.displayProjection, map.projection), zoom);  
                },
        
                onPopupClose: function(evt) {
                        // 'this' is the popup.
                        selectControl.unselect(this.feature);
                }
        };
}


        
        


