(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
    ({key: "AIzaSyAYmZTsDBcG751atHJ5iJTOzdaGjwpUe60", v: "beta"});

document.addEventListener("DOMContentLoaded", async function () {
    let map;
    let marker;
    let infoWindow;

    // Fetch cafe data from the backend
    const response = await fetch('/api/cafes/');
    const cafes = await response.json();
    const googlePlaceIds = cafes.map(cafe => cafe.google_place_id);

    async function initMap() {
        // Request needed libraries.
        //@ts-ignore
        const [{ Map }, { AdvancedMarkerElement }] = await Promise.all([
            google.maps.importLibrary("marker"),
            google.maps.importLibrary("places"),
        ]);

        // Initialize the map.
        const origin = { lat: 52.091664, lng: 5.121118 };
        map = new google.maps.Map(document.getElementById("map"), {
            center: origin,
            zoom: 10,
            mapId: "2835c76151db33b6",
            mapTypeControl: false,
        });

        // If available, set the map to the user's current position.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                currentLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                map.setCenter(currentLocation);
            })
        };

        // Add markers for cafes
        cafes.forEach(cafe => {
            const marker = new google.maps.marker.AdvancedMarkerElement({
                map: map,
                position: { lat: cafe.latitude, lng: cafe.longitude },
                title: cafe.name,
            });

            // InfoWindow for each marker
            infoWindow = new google.maps.InfoWindow({});

            let content = createContentForInfoWindow(cafe.google_place_id, cafe.name, cafe.address, googlePlaceIds);

            marker.addListener("gmp-click", () => {
                infoWindow.setContent(content);
                infoWindow.open(map, marker);
            });
        });

        //@ts-ignore
        const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement({
            componentRestrictions: {country: ['nl']},
            types: ['bakery', 'cafe', 'restaurant'],
        });

        //@ts-ignore
        placeAutocomplete.id = "place-autocomplete-input";

        const card = document.getElementById("place-autocomplete-card");

        //@ts-ignore
        card.appendChild(placeAutocomplete);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(card);

        // Create the marker and infowindow
        marker = new google.maps.marker.AdvancedMarkerElement({
            map: map,
        });
        infoWindow = new google.maps.InfoWindow({});

        // Add the gmp-placeselect listener, and display the results on the map.
        //@ts-ignore
        placeAutocomplete.addEventListener("gmp-placeselect", async ({ place }) => {
            await place.fetchFields({
            fields: ["id", "displayName", "formattedAddress", "location"],
            });

            // If the place has a geometry, then present it on a map.
            if (place.viewport) {
                map.fitBounds(place.viewport);
            } else {
                map.setCenter(place.location);
                map.setZoom(17);
            };

            let content = createContentForInfoWindow(place.id, place.displayName, place.formattedAddress, googlePlaceIds);

            updateInfoWindow(infoWindow, content, place.location);
            marker.position = place.location;
            marker.title = place.displayName;
        });

        new ClickEventHandler(map, origin);
    };

    function isIconMouseEvent(e) {
        return "placeId" in e;
        }

    class ClickEventHandler { // TODO: Use new Places API
        origin;
        map;
        placesService;
        infowindow;
        infowindowContent;
        constructor(map, origin) {
            this.origin = origin;
            this.map = map;
            this.placesService = new google.maps.places.PlacesService(map);
            this.infowindow = new google.maps.InfoWindow();
            this.infowindowContent = document.getElementById("infowindow-content");
            this.infowindow.setContent(this.infowindowContent);
            // Listen for clicks on the map.
            this.map.addListener("click", this.handleClick.bind(this));
        };
        handleClick(event) {
            // If the event has a placeId, use it.
            if (isIconMouseEvent(event)) {
                // Calling e.stop() on the event prevents the default info window from
                // showing.
                // If you call stop here when there is no placeId you will prevent some
                // other map click event handlers from receiving the event.
                event.stop();
                if (event.placeId) {
                    this.getPlaceInformation(event.placeId);
                }
            }
        };
        getPlaceInformation(placeId) {
            const me = this;

            this.placesService.getDetails({ placeId: placeId, language: 'nl' }, (place, status) => {
                if (
                    status === "OK" &&
                    place &&
                    place.geometry &&
                    place.geometry.location
                ) {
                    me.infowindow.close();
                    let content = createContentForInfoWindow(place.place_id, place.name, place.formatted_address, googlePlaceIds)
                    updateInfoWindow(me.infowindow, content, place.geometry.location)
                    me.infowindow.open(me.map);
                }
            });
        };
    };


    // Helper function to create an info window.
    function updateInfoWindow(infoWindow, content, position) {
        infoWindow.setContent(content);
        infoWindow.setPosition(position);
        infoWindow.open({
            map,
            anchor: marker,
            shouldFocus: false,
        });
    };

    // Helper function to create content for info window.
    function createContentForInfoWindow(id, name, address, googlePlaceIds) {
        let detailUrl = cafeDetailUrl.replace('PLACE_ID_PLACEHOLDER', id);
        let reviewUrl = addReviewUrl.replace('PLACE_ID_PLACEHOLDER', id).replace('PLACE_NAME_PLACEHOLDER', name);

        let nameEl = '<h4 id="place-displayname" class="title">' + name + '</h4>';
        let addressEl = '<span id="place-address">' + address + '</span>';
        let reviewEl = `<a href="${reviewUrl}">Write a review</a>`;
        let ratingEl;

        if (googlePlaceIds.includes(id)) {
            let cafe = cafes[cafes.findIndex(cafe => cafe.google_place_id === id)];
            let ratingsNo = cafe.number_of_ratings;
            let rating = cafe.rating;
            let roundedRating = Math.round(rating * 2) / 2;
            let fullStars = Math.floor(roundedRating);
            let halfStar = roundedRating % 1 !== 0 ? 1 : 0;
            let emptyStars = 5 - (fullStars + halfStar);
            ratingEl = `<a href="${detailUrl}" style="text-decoration:none">` + `<span class="fa-solid fa-star"></span>`.repeat(fullStars) + (halfStar ? `<span class="fa-regular fa-star star"></span>` : ``) + `<span class="fa-regular fa-star"></span>`.repeat(emptyStars) + ` (${ratingsNo} ratings)` + `</a><br/>`;
        } else {
            ratingEl = '';
        };

        let content = '<div id="infowindow-content">' + nameEl + ratingEl + '<br/>' + addressEl + '<br/><br/>' + reviewEl + '</div>';

        return content;
    };

    initMap();

});