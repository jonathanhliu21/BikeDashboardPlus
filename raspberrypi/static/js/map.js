var mymap = L.map('mapid').setView(['39.7392', '104.9903'], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/jonyboi396825/ckr5pbzyq1n4t17mo8g4ykvr8.html?fresh=true&title=view&access_token=pk.eyJ1Ijoiam9ueWJvaTM5NjgyNSIsImEiOiJja3F2cjBmZ2gwaDVtMnZ0Zm9nNmtmd2xiIn0.1imQCah8Gzp6HP_EJKKgmA', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(mymap);

// mapbox://styles/jonyboi396825/ckr5pbzyq1n4t17mo8g4ykvr8