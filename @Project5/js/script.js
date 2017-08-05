var map;

var markers = [];
// Create a new blank array for all the listing markers.
var defaultIcon;
var highlightedIcon;
var largeInfowindow;

function googleError(event) {
  window.alert("Cannot load google map, please check your connection");
}

function initMap() {
  var self=this;
  // Constructor creates a new map - only center and zoom are required.
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 40.7413549, lng: -73.9980244},
    zoom: 13,
    styles: styles,
    mapTypeControl: false
  });

  var bounds = new google.maps.LatLngBounds();
  largeInfowindow = new google.maps.InfoWindow();
  // Style the markers a bit. This will be our listing marker icon.
  defaultIcon = makeMarkerIcon('0091ff');
  highlightedIcon = makeMarkerIcon('FFFF24');
  this.locationDetail = [];
  // The following group uses the location array to create an array of markers on initialize.
  for (var i = 0; i < locations.length; i++) {
    // Get the position from the location array.
    var position = locations[i].location;
    var title = locations[i].title;
    var marker = new google.maps.Marker({
      position: position,
      title: title,
      animation: google.maps.Animation.DROP,
      icon: defaultIcon,
      id: i
    });
    // Push the marker to our array of markers.
    markers.push(marker);
    locations[i].marker = marker;
    // Create an onclick event to open the large infowindow at each marker.

    marker.addListener('click', function() {
      populateInfoWindow(this, largeInfowindow, locationDetail);
      toggleBounce(this);
      this.setIcon(highlightedIcon);

      var position = this.getPosition();
      var title = this.title;
      var foursquareUrl = "https://api.foursquare.com/v2/venues/search" +
      "?client_id=0TMXE0I1J40KIQZ05CKQZIKBCDVJA1PI52DFVESQIF2BNPZW" +
      "&client_secret=WXGYSZAYYVFEHWRII10J1URGBZ3C5OZ3HXVM5MZTQO1R41YQ" +
      "&v=20130815" +
      "&m=foursquare" +
      "&ll=" + position.lat() + "," + position.lng() +
      "&query=" + title.split(' ').join('');

      $.ajax({
          type:'GET',
          url:foursquareUrl,
          dataType:'json',
          async:true,
          success:function(JSONdata){

        if(JSONdata.response.venues){
          var item = JSONdata.response.venues[0];
          if (item)
            locationDetail = {name: item.name, address: item.location.address, zipcode: item.location.postalCode };
          else 
            locationDetail = {name: null, address: "Cannot Retrieve Data from Foursquare"};
        } else {
          locationDetail = {name: null, address: "Cannot Retrieve Data from Foursquare"};
          alert("Something went wrong, Could not retreive data from foursquare. Please try again!");
        }
        AVM.listDetail(locationDetail);
        }
      }).fail(function(){
          alert("Something went wrong, Could not retreive data from foursquare. Please try again!"); 
      });

    AVM.showDetail(true);

    });
    marker.setMap(map);
    bounds.extend(markers[i].position);
  }
  map.fitBounds(bounds);
}

// This function populates the infowindow when the marker is clicked. We'll only allow
// one infowindow which will open at the marker that is clicked, and populate based
// on that markers position.
function populateInfoWindow(marker, infowindow) {
  // Check to make sure the infowindow is not already opened on this marker.
  if (infowindow.marker != marker) {
    // Clear the infowindow content to give the streetview time to load.
    infowindow.setContent('');
    // infowindow.marker.setIcon(defaultIcon);
    // console.log(infowindow.marker);
    if(infowindow.marker) {
      infowindow.marker.setIcon(defaultIcon);
    }
    infowindow.marker = marker;
    // Make sure the marker property is cleared if the infowindow is closed.
    infowindow.addListener('closeclick', function() {
      marker.setIcon(defaultIcon);
      infowindow.marker = null;
    });
    var streetViewService = new google.maps.StreetViewService();
    var radius = 50;
    // In case the status is OK, which means the pano was found, compute the
    // position of the streetview image, then calculate the heading, then get a
    // panorama from that and set the options
    // Use streetview service to get the closest streetview image within
    // 50 meters of the markers position
    // streetViewService.getPanoramaByLocation(marker.position, radius, getStreetView);
    streetViewService.getPanoramaByLocation(marker.position, radius, function (data, status) {
      var content = '<div>' + marker.title + '</div>';
      if (status == google.maps.StreetViewStatus.OK) {
        var nearStreetViewLocation = data.location.latLng;
        content = content + '<div id="pano"></div>';
        var heading = google.maps.geometry.spherical.computeHeading(
          nearStreetViewLocation, marker.position);
          infowindow.setContent(content);
          var panoramaOptions = {
            position: nearStreetViewLocation,
            pov: {
              heading: heading,
              pitch: 30
            }
          };
        var panorama = new google.maps.StreetViewPanorama(
        document.getElementById('pano'), panoramaOptions);
      } else {
        infowindow.setContent(content + '<div>No Street View Found</div>');
      }
    });
    // Open the infowindow on the correct marker.
    infowindow.open(map, marker);
  }
}

// This function takes in a COLOR, and then creates a new marker
// icon of that color. The icon will be 21 px wide by 34 high, have an origin
// of 0, 0 and be anchored at 10, 34).
function makeMarkerIcon(markerColor) {
  var markerImage = new google.maps.MarkerImage(
    'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
    '|40|_|%E2%80%A2',
    new google.maps.Size(21, 34),
    new google.maps.Point(0, 0),
    new google.maps.Point(10, 34),
    new google.maps.Size(21,34));
  return markerImage;
}

