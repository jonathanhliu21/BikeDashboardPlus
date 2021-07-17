var tot_dist = 0;

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
    var dist = 0;
    var prev_cor = arr[0];
    for (let i = 0; i < arr.length; i++){
        let cur_cor = arr[i];
        if (cur_cor == "PAUSED" && i === arr.length-1) break;

        // console.log("before", i, cur_cor, prev_cor)
        if (cur_cor === "PAUSED" && i !== arr.length-1){
            prev_cor = arr[i+1];
            continue;
        } else{
            dist += get_dist_lat_lon(cur_cor, prev_cor);
        }
        // console.log(i, cur_cor, prev_cor, dist, get_dist_lat_lon(cur_cor, prev_cor));

        prev_cor = cur_cor;
    }

    return dist;
}

function conv_dist_unit(dist, unit){
    if (unit === "0"){
        return (dist/1609).toFixed(6);
    } else{
        return (dist/1000).toFixed(3);
    }
}

function handle_track_data(s, unit){
    var arr = s.trimEnd().split("\n");
    var dist = calc_tot_dist(arr);

    var start_cor = arr[0];
    var end_cor = arr[arr.length-1];

    var mymap = L.map('mapid').setView(start_cor.trim().split(","), 15);

    L.tileLayer('https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
        tileSize: 512,
        zoomOffset: -1,
        detectRetina: true
    }).addTo(mymap); 

    L.marker(start_cor.trim().split(","), {
        title: 'start',
        icon: new L.Icon({
            iconUrl: "/static/img/start.png",
            iconSize: 40
        })
    }).addTo(mymap);

    L.marker(end_cor.trim().split(","), {
        title: 'end',
        icon: new L.Icon({
            iconUrl: "/static/img/end.png",
            iconSize: 40
        })
    }).addTo(mymap);

    var ptr = 0; 
    while (ptr < arr.length){
        let coords = [];
        while (ptr < arr.length && arr[ptr] !== "PAUSED"){
            coords.push(arr[ptr].trim().split(","));
            ptr++;
        }

        L.polyline(coords, {
            color: "red",
            smoothFactor: "4.0"
        }).addTo(mymap);

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

        if (coords[coords.length-1][0] !== s2[0] || coords[coords.length-1][1] !== s2[1]){
            L.marker(coords[coords.length-1], {
                title: 'paused',
                icon: new L.Icon({
                    iconUrl: "/static/img/pause.png",
                    iconSize: 40
                })
            }).addTo(mymap);
        }

        while (ptr < arr.length && arr[ptr] === "PAUSED"){
            ptr++;
        }
    }

    var unit_str = (unit == 0 ? "mi" : "km");
    var dist_str = "Total distance: ".concat(String(conv_dist_unit(dist, unit)), unit_str)

    new Vue({
        el: "#dist",
        delimiters: ["[[", "]]"],
        data: {
            distance: dist_str
        }
    });
}


