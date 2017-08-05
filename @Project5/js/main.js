var AppViewModel = function() {
  var cityStr = "NewYork";
  var nytimesUrl = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + cityStr + "&sort=newest&api-key=e6911fade1c344cb9cac21820250d058";
  var self = this;

  self.allLocations = ko.observableArray(locations);
  self.initFlag = ko.observable(true);
  self.articlesArray = ko.observableArray([]);

  $.getJSON(nytimesUrl, function(data) {
      articles = data.response.docs;
      for (var i = 0; i < articles.length; i++) {
        self.articlesArray.push( articles[i]);
      }
   }).fail(function (e) {
      window.alert('New York Times Articles Could Not Be Loaded');
   });

  self.map = ko.observable(map);
  self.filter =  ko.observable("");
  self.search = ko.observable("");
  self.slidedFlag = ko.observable(false);
  self.filteredArray = ko.computed(function() {
    return ko.utils.arrayFilter(self.allLocations(), function(item) {
          var show = item.title.toLowerCase().indexOf(self.filter().toLowerCase()) !== -1;
          if (item.marker) {
              item.marker.setVisible(show); 
          }
          return show;
    });
  }, self);

  self.listDetail = ko.observable();
  self.showDetail = ko.observable();
  self.clickHandler = function(data) {
    centerLocation(data,  self.allLocations);

    var position = data.location;
    var title = data.title;
    var foursquareUrl = "https://api.foursquare.com/v2/venues/search" +
      "?client_id=0TMXE0I1J40KIQZ05CKQZIKBCDVJA1PI52DFVESQIF2BNPZW" +
      "&client_secret=WXGYSZAYYVFEHWRII10J1URGBZ3C5OZ3HXVM5MZTQO1R41YQ" +
      "&v=20130815" +
      "&m=foursquare" +
      "&ll=" + position.lat + "," + position.lng +
      "&query=" + title.split(' ').join('');
      $.ajax({
        type:'GET',
        url:foursquareUrl,
        dataType:'json',
        async:true,
        success:function(JSONdata){

      if(JSONdata.response.venues){
        var item = JSONdata.response.venues[0];
        // console.log(item);
        if (item)
          locationDetail = {name: item.name, address: item.location.address, zipcode: item.location.postalCode };
        else 
          locationDetail = {name: null, address: "Cannot Retrieve Data from Foursquare"};
      } else {
        locationDetail = {name: null, address: "Cannot Retrieve Data from Foursquare"};
        alert("Something went wrong, Could not retreive data from foursquare. Please try again!");
      }
      self.listDetail(locationDetail);
      }
    }).fail(function(){
        alert("Something went wrong, Could not retreive data from foursquare. Please try again!"); 
    });
    self.showDetail(true);
  };

  self.sliding = function(data, element) {
    self.slidedFlag(!self.slidedFlag());
  };
};
var AVM = new AppViewModel();
ko.applyBindings(AVM);

function toggleBounce(marker) {
  // Google map documentation shows to keep one "=" instead of two. Does not work with "=="
  if (marker.getAnimation() !== null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(function() {
      marker.setAnimation(null);
    }, 2100);
  }
}

function centerLocation(data, thisLocations) {

  var latlng = new google.maps.LatLng(data.location.lat, data.location.lng);
  // thisMap.setCenter(latlng);
  map.setCenter(latlng);
  map.setZoom(12);
  for (var i = 0; i < thisLocations().length; i++) {
    if (data.title === thisLocations()[i].title) {
      toggleBounce(thisLocations()[i].marker);
      thisLocations()[i].marker.setIcon(highlightedIcon);
      populateInfoWindow(thisLocations()[i].marker, largeInfowindow);
    }
  }
}