import {useEffect, useState} from "react";
import {Circle, MapContainer, Marker, Popup, TileLayer, useMap, useMapEvents} from 'react-leaflet';
import L, {LatLng} from 'leaflet';
import "leaflet/dist/leaflet.css";

function LocationMarker() {
    const [position, setPosition] = useState(null)
    const locationIcon = L.icon({
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        iconAnchor: [12.5, 41],
        popupAnchor: [0, -41],
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        shadowSize: [41, 41],
        shadowAnchor: [12.5, 41]
    });
    const map = useMapEvents({
        layeradd: () => {
            if(!position)
                map.locate()
        },
        locationfound(e:any) {
            setPosition(e.latlng)
            map.flyTo(e.latlng, map.getZoom())
        },
    })
    return position === null ? null : (
        //@ts-ignore
        <Marker position={position} icon={locationIcon}>
            <Popup>Twoja lokalizacja</Popup>
        </Marker>
    )
}

function StationMarker(props:{id:string, name:string, lat:number, lon:number, pollution:[{indicator:string, value:number, date:string, unit:string}]}) {
    const [status, setStatus] = useState(0.0);
    const i_names = ["PM10", "PM25", "NO2", "SO2", "CO", "O3", "C6H6"];
    const pollutionMax = {
        "PM10": 50,
        "PM25": 25,
        "NO2": 200,
        "SO2": 350,
        "CO": 10000,
        "O3": 120,
        "C6H6": 5
    }
    useEffect(() => {
        let state_temp=0;
        for(let i = 0; i < props.pollution.length; i++) {
            let indicator = props.pollution[i].indicator;
            if(i_names.includes(indicator)) {
                state_temp += props.pollution[i].value / pollutionMax[indicator as keyof typeof pollutionMax];
            }
        }
        setStatus(state_temp);
    }, [props.pollution, i_names, pollutionMax]);
    return (
        <Circle center={[props.lat, props.lon]} radius={50000} fillOpacity={0.05} opacity={0.1} pathOptions={{color: `hsl(${(130-status*30)>=0?(130-status*30):0},100%,50%)`}}>
            <Popup>
                <div>
                    <h1>{props.name}</h1>
                    <p>Pomiary:</p>
                    <ul>
                        {props.pollution.map((p, i) => <li key={i}>{p.indicator}: {p.value} {p.unit} ({p.date})</li>)}
                    </ul>
                </div>
            </Popup>
        </Circle>
    )
}

function Stations(){
    const [stations, setStations] = useState<{
        id:string,
        latitude:number,
        longitude:number,
        name:string,
        pollution:[{indicator:string, value:number, date:string, unit:string}]
    }[]>([]);
    const [previousPosition, setPreviousPosition] = useState<{latitude:number, longitude:number}>();
    const [date, setDate] = useState<Date>(new Date("2018-01-01"));
    const fetchData = (size:number, currentPosition:LatLng, dateFormatted:string) => {
            fetch(`http://127.0.0.1:5000/nearby?latitude=${currentPosition.lat}&longitude=${currentPosition.lng}&maxDistance=${size}&from=${dateFormatted}&to=${dateFormatted}`)
                .then(response => response.json())
                .then(data => setStations(data))
            setPreviousPosition({latitude: currentPosition.lat, longitude: currentPosition.lng})
    }
    useMapEvents({
        moveend: (event) => {
            const currentPosition = event.target.getCenter();
            if(previousPosition == null || currentPosition.distanceTo(new LatLng(previousPosition.latitude,previousPosition.longitude)) > 100000) {
                const size = Math.max(event.target.getBounds().getNorth() - event.target.getBounds().getSouth(), event.target.getBounds().getEast() - event.target.getBounds().getWest())*111.32;
                //@ts-ignore
                const dateFormatted = date.toLocaleDateString("en-GB", {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                }).replaceAll("/", "-");
                fetchData(size, currentPosition, dateFormatted)
            }
        },
        //@ts-ignore
        timechange: (event) => {
            setDate(new Date(event.time))
            const size = Math.max(event.target.getBounds().getNorth() - event.target.getBounds().getSouth(), event.target.getBounds().getEast() - event.target.getBounds().getWest())*111.32;
            const currentPosition = event.target.getCenter();
            //@ts-ignore
            const dateFormatted = new Date(event.time).toLocaleDateString("en-GB", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
            }).replaceAll("/", "-");
            fetchData(size, currentPosition, dateFormatted)
        }
    })
    console.log(stations)
    return (
        <>
            {
                stations.map(station => <StationMarker key={station.id} id={station.id} name={station.name} lat={station.latitude} lon={station.longitude} pollution={station.pollution}/>)
            }
        </>
    )
}

function TimeRangeSlider() {
    const map = useMap();
    useEffect(() => {
        //@ts-ignore
        L.Control.TimeSlider = L.Control.extend({
            onAdd: function() {
                if(document.getElementById("time-control") != null)
                    return document.getElementById("time-control");
                const div = L.DomUtil.create('div', 'time-control leaflet-bar leaflet-control rounded relative pt-1');
                div.id = "time-control";
                const label = L.DomUtil.create('label', "form-label", div);
                label.id="time-label";
                label.innerText = "Data: ";
                const input = L.DomUtil.create('input', "form-range appearance-none w-full h-6 p-1 bg-gray-200 focus:outline-none focus:ring-0 focus:shadow-none rounded-full", div);
                input.id = "time-input";
                input.type = "date";
                input.value = "2018-01-01";
                input.min="2000-01-01";
                input.max="2021-12-31";
                L.DomEvent.disableClickPropagation(div);
                L.DomEvent.disableScrollPropagation(div);
                L.DomEvent.on(input, 'change', (e:any) => {
                    map.fire("timechange", {time: e.target.value});
                })
                return div;
            },
            onRemove: function() {

            }
        });

        //@ts-ignore
        L.control.TimeSlider = function(opts) {
            //@ts-ignore
            return new L.Control.TimeSlider(opts);
        }
        //@ts-ignore
        L.control.TimeSlider().addTo(map);
    })
    return (
        <div>
        </div>
    )
}

export default function AirPollutionMap() {
    return (
        //@ts-ignore
        <MapContainer center={[54.370, 18.630]} zoom={8} scrollWheelZoom={true} className="h-[91.5vh] w-[98.5vw]">
            <LocationMarker/>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Stations/>
            <TimeRangeSlider/>
        </MapContainer>
    )
}