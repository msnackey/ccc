(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
    ({key: "AIzaSyAYmZTsDBcG751atHJ5iJTOzdaGjwpUe60", v: "beta"});

document.addEventListener("DOMContentLoaded", async function () {
    let map;
    let marker;
    let infoWindow;

    async function initMap() {
        // Fetch cafe data from the backend
        const response = await fetch('/api/cafes/');
        const cafes = await response.json();
        const googlePlaceIds = cafes.map(cafe => cafe.google_place_id);

        // Request needed libraries.
        //@ts-ignore
        const [{ Map }, { AdvancedMarkerElement }] = await Promise.all([
            google.maps.importLibrary("marker"),
            google.maps.importLibrary("places"),
        ]);

        // Initialize the map.
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 52.091664, lng: 5.121118 },
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

            updateInfoWindow(content, place.location);
            marker.position = place.location;
            marker.title = place.displayName;
        });
    };

    // Helper function to create an info window.
    function updateInfoWindow(content, position) {
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
        let reviewUrl = addReviewUrl.replace('PLACE_ID_PLACEHOLDER', id);

        let nameElement = '<span id="place-displayname" class="title">' + name + '</span>';
        let addressElement = '<span id="place-address">' + address + '</span>';
        let reviewElement = `<a href="${reviewUrl}">Write a review</a>`;
        let detailsElement;

        if (googlePlaceIds.includes(id)) {
            detailsElement = `<a href="${detailUrl}">Show details</a>`;
        } else {
            detailsElement = '';
        };

        let content = '<div id="infowindow-content">' + nameElement + '<br/>' + addressElement + '<br/><br/>' + detailsElement + '<br/>' + reviewElement + '</div>';

        return content;
    };

    initMap();

});