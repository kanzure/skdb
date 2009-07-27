

function LatLonSelector() {
        var latitude;
        var longitude;
        var map;
        var marker;
        var control;
        
        return {
                init: function(mape, latelement, lonelement) {
                        // Map is a instance of the Map class from Map.js
                        // Latelement and lonelement are JQuery objects referring to <input> boxes or similar.
                        map = mape;
                        var markers = new OpenLayers.Layer.Markers("Lat/Lon selector");
                        marker = map.createMarker(0, 0);
                        markers.addMarker(marker);
                        map.getMap().addLayer(markers);
                        
                        control = new OpenLayers.Control.DragMarker(markers, {'onComplete': function() { this.onComplete(); }, 'onDrag': function() { this.onDrag(); }});
                        map.getMap().addControl(control);
                        control.activate();
                },
                
                onComplete: function(layer, pixel) {
                        var lonlat = map.getLonLatFromViewPortPx(pixel.x, pixel.y);
                        alert("You dropped it near " + lonlat.lat + " N, " + lonlat.lon + " E");                
                },
                
                onDrag: function(layer, pixel) {
                },
                
                activate: function() {
                        control.activate();
                },
                
                deactivate: function() {
                        control.deactivate();
                },
                
                setLocation: function(lat, lon) {
                        
                },
                
                getLocation: function() {
                        
                },
                
                update: function() {
                        
                }
        };
}