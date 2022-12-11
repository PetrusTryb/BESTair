import React, {useEffect, useState} from "react";

export default function StationDetails() {
    const [station, setStation] = useState<{
        latitude:number,
        longitude:number,
        name:string
    }>();
    const [pollution, setPollution] = useState<[{indicator:string, value:number, date:string, unit:string}]>();
    //const [dateFrom, setDateFrom] = useState<Date>(new Date("2018-01-01"));
    //const [dateTo, setDateTo] = useState<Date>(new Date("2019-01-01"));
    const stationId = window.location.search.split("=")[1];
    const fetchStation = async () => {
        try {
            const response = await fetch(`http://localhost:5000/station/${stationId}`);
            const data = await response.json();
            setStation(data);
            const pollutionResponse = await fetch(`http://localhost:5000/pollution/${stationId}`);
            const pollutionData = await pollutionResponse.json();
            setPollution(pollutionData);
        } catch (e) {
            console.error(e);
        }
    }
    useEffect(() => {
        if(!station){
            fetchStation();
        }
    });
    return (
        <div>
            <div className="text-2xl">
                {station?.name}
            </div>
            <div className="text-xl">
                {station?.latitude}, {station?.longitude}
            </div>
            <div className="text-xl">
                Pomiary:
            </div>
            <table className="table-auto min-w-full">
                <thead className="border-b">
                    <tr>
                        <th>Data pomiaru</th>
                        <th>Parametr</th>
                        <th>Wartość</th>
                    </tr>
                </thead>
                <tbody>
                {pollution?.map((pollution) => {
                    if(pollution.value != null) {
                        return (
                            <tr key={pollution.date}>
                                <td>{pollution.date}</td>
                                <td>{pollution.indicator}</td>
                                <td>{pollution.value} {pollution.unit}</td>
                            </tr>
                        )
                    }
                })
                }
                </tbody>
            </table>
            <div className="flex flex-wrap justify-center">

            </div>
        </div>
    );
}