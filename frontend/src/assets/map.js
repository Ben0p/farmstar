mapboxgl.accessToken = 'pk.eyJ1IjoiYmVuMCIsImEiOiJjajh1ZDMzNzkweXU5MnJvNmNjOGE1c3UzIn0.lj3vfW_n49fbhc1V46qfUA';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/ben0/cjjpgd5f8112m2ro48usu10ov',
    zoom: 0
});

map.addControl(new mapboxgl.NavigationControl());
map.addControl(new mapboxgl.GeolocateControl());


var url = 'http://127.0.0.1:8001';
var url2 = 'http://127.0.0.1:8001/geoline';
var url3 = 'http://127.0.0.1:8001/xIMs';

map.on('load', function () {

    map.addSource('drone', { type: 'geojson', data: url });
	map.addSource('drone_path', { type: 'geojson', data: url2 });
	map.addSource('xIMs', { type: 'geojson', data: url3 });

    window.setInterval(function() {
        map.getSource('drone').setData(url);
		map.getSource('drone_path').setData(url2);
		map.getSource('xIMs').setData(url3);
    }, 1000);



    map.addLayer({
        "id": "drone",
        "type": "symbol",
        "source": "drone",
        "layout": {
            "icon-image": "tractor-planting"
        },
		"includeGeometry": "true"
    });
    map.addLayer({
        "id": "route",
        "type": "line",
        "source": "drone_path",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "#888",
            "line-width": 8
        }
    });
    map.addLayer({
        "id": "Trucks",
        "type": "symbol",
        "source": "xIMs",
        "layout": {
            "icon-image": "rocket-15"
        },
		"includeGeometry": "true"
    });
	

	
});
