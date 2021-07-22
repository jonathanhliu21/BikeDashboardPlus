function get_dist_lat_lon(s1, s2){
    // get coordinates from strings
    const cor1 = s1.trim().split(",");
    const cor2 = s2.trim().split(",");

    // parse coordinates as floats
    const la1 = parseFloat(cor1[0]);
    const lo1 = parseFloat(cor1[1]);
    const la2 = parseFloat(cor2[0]);
    const lo2 = parseFloat(cor2[1]);

    // uses the haversine formula and returns in meters
    // code below and formula info from http://www.movable-type.co.uk/scripts/latlong.html

    const R = 6371e3; // radius of earth in meters
    const p1 = la1*Math.PI/180;
    const p2 = la2*Math.PI/180;
    const dp = (la2-la1)*Math.PI/180;
    const dl = (lo2-lo1)*Math.PI/180;

    const a = Math.sin(dp/2)*Math.sin(dp/2) + Math.cos(p1)*Math.cos(p2)*Math.sin(dl/2)*Math.sin(dl/2);
    const c = 2*Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    const d = R*c;

    return d;
}

function calc_tot_dist(arr){
    // given arr of coordinates, find total distance
    var dist = 0;
    var prev_cor = arr[0];
    for (let i = 0; i < arr.length; i++){
        let cur_cor = arr[i];

        if (cur_cor === "PAUSED" && i !== arr.length-1){
            // if paused, put the previous ptr to the next element so the previous ptr wouldn't be "PAUSED"
            // continue or else it will assign prev ptr to "PAUSED"

            prev_cor = arr[i+1];
            continue;
        } else if (cur_cor == "PAUSED" && i === arr.length-1) {
            // don't need to track if last element is paused

            break;
        } else{
            // if no pause, add distance between cur coordinate and prev coordinate

            dist += get_dist_lat_lon(cur_cor, prev_cor);
        }

        prev_cor = cur_cor;
    }

    return dist;
}

function conv_dist_unit(dist, unit){
    // takes in dist as meters and returns distance in km or miles

    if (unit === "0"){
        return (dist/1609).toFixed(3); // mi
    } else{
        return (dist/1000).toFixed(3); // km
    }
}

function conv_sm_dist_unit(dist, unit){
    // takes in distance in m and converts it to m or ft
    var dist_in_big_unit = conv_dist_unit(dist, unit);

    if (unit === "0"){
        var trailing_miles = dist_in_big_unit-Math.floor(dist_in_big_unit);
        // variable will be something like 0.124 (not greater than 1)  
        //                   need to convert ^^^ to ft by multiplying by 5280 

        return (trailing_miles*5280).toFixed(3); // prevent floating point error
    } else {
        var trailing_km = dist_in_big_unit-Math.floor(dist_in_big_unit);
        // variable will be something like 0.124 (not greater than 1)  
        //                   need to convert ^^^ to meters by multiplying by 1000 

        return (trailing_km*1000).toFixed(3); // prevent floating point error
    }
}

function handle_track_data(s, unit){
    // takes in file string and cfg unit from flask jinja

    var arr = s.trimEnd().split("\n");
    // if last element is "PAUSED"
    while (arr.length > 0 && (arr[arr.length-1] === "PAUSED" || arr[arr.length-1] === "")) arr.pop();

    // put delete button on DOM and put msg if the file has data error
    new Vue({
        el: "#data_err",
        delimiters: ["[[", "]]"],
        data: {
            text: (arr.length <= 0 ? "See weird text? No map? That's because there is a data error. Consider deleting the file." : "")     
        },
        methods: {
            // warns user if they actually want to delete file
            warn: function(){
                var cur_file = window.location.pathname.slice(5, window.location.pathname.length);

                var pressed = confirm("Are you sure you want to delete this file PERMANENTLY? There will be NO WAY to recover this file.");
                if (pressed){
                    // POST request to delete endpoint
                    axios.post(`/map/delete/${cur_file}`, {})
                    .then((response) => {
                        alert("Successfully deleted");
                        window.location.href = "/map";
                    })
                    .catch((error) => {
                        alert("Error in deleting: ".concat(error));
                    });
                } 
            }
        }
    });

    // data error = file has only "PAUSED" or is empty, and has no coordinates
    if (arr.length <= 0){
        return;
    }

    var dist = calc_tot_dist(arr); // calculate distance

    // starting and ending coordinates
    var start_cor = arr[0];
    var end_cor = arr[arr.length-1];

    // initialize map
    var mymap = L.map('mapid').setView(start_cor.trim().split(","), 15);

    L.tileLayer('https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        minZoom: 1,
        maxZoom: 19,
        tileSize: 512,
        zoomOffset: -1,
        detectRetina: true
    }).addTo(mymap); 

    // start marker on map
    L.marker(start_cor.trim().split(","), {
        title: 'start',
        icon: new L.Icon({
            iconUrl: "/static/img/start.png",
            iconSize: 40
        })
    }).addTo(mymap);

    // end marker on map
    L.marker(end_cor.trim().split(","), {
        title: 'end',
        icon: new L.Icon({
            iconUrl: "/static/img/end.png",
            iconSize: 40
        })
    }).addTo(mymap);

    // while loop to add polylines (track lines) and paused/resumed markers to map
    var ptr = 0; 
    while (ptr < arr.length){
        let coords = [];

        // keep on putting all coordinates into arr until paused
        while (ptr < arr.length && arr[ptr] !== "PAUSED"){
            coords.push(arr[ptr].trim().split(","));
            ptr++;
        }

        // display coordinates as polyline
        L.polyline(coords, {
            color: "blue",
            smoothFactor: "4.0"
        }).addTo(mymap);

        // you can tell that the coords are a resumed track path by comparing the first element of
        // coords[] to the start coordinates
        // if it is resumed, put a "resumed" marker at the coordinates of the first element of coords[]
        let s1 = start_cor.trim().split(",");
        let s2 = end_cor.trim().split(",");
        if (coords[0][0] !== s1[0] || coords[0][1] !== s1[1]){
            L.marker(coords[0], {
                title: 'resumed',
                icon: new L.Icon({
                    iconUrl: "/static/img/resume.png",
                    iconSize: 40
                })
            }).addTo(mymap);
        }

        // similar to above, you can tell if the current coords[] arr was paused by comparing the last
        // element to the ending coordinates
        // if paused, put a marker at the ending coordinates
        if (coords[coords.length-1][0] !== s2[0] || coords[coords.length-1][1] !== s2[1]){
            L.marker(coords[coords.length-1], {
                title: 'paused',
                icon: new L.Icon({
                    iconUrl: "/static/img/pause.png",
                    iconSize: 40
                })
            }).addTo(mymap);
        }

        // move ptr if paused so it is not an infinite loop
        while (ptr < arr.length && arr[ptr] === "PAUSED"){
            ptr++;
        }
    }

    var unit_str = (unit == 0 ? "mi" : "km");

    // excess meters/feet (10.6 km -> 10 km 600 m)
    var smaller_val = conv_sm_dist_unit(dist, unit);
    var smaller_unit = (unit == 0 ? "ft" : "m");

    // put total distance on DOM
    new Vue({
        el: "#dist",
        delimiters: ["[[", "]]"],
        data: {
            distance1: conv_dist_unit(dist, unit),
            distance2: smaller_val,
            unit1: unit_str,
            unit2: smaller_unit 
        }
    });

    // raw tracking data
    new Vue({
        el: "#raw_data",
        delimiters: ["[[", "]]"],
        data: {
            arr_: arr
        }
    });
}
