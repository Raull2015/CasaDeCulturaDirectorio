var map;

function initMap() {

    var latlng = new google.maps.LatLng(53.385873, -1.471471);

    var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    var beachMarker = new google.maps.Marker({
        position: {lat: 53.385873, lng: -1.471471},
        map: map,
        icon: image
    });

    var styles = [
    {
        featureType: "landscape",
        stylers: [
        { color: '#eeddee' }
        ]
    },{
        featureType: "natural",
        stylers: [
        { hue: '#ff0000' }
        ]
    },{
        featureType: "road",
        stylers: [
        { hue: '#5500aa' },
        { saturation: -70 }
        ]
    },{
        featureType: "building",
        elementType: "labels",
        stylers: [
        { hue: '#000066' }
        ]
    },{
        featureType: "poi", //points of interest
        stylers: [
        { hue: '#0044ff' }
        ]
    }
    ];


    var myOptions = {
        zoom: 14,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true,
        styles: styles,
        scrollwheel:  false
    };

    map = new google.maps.Map(document.getElementById('map'), myOptions);
}




