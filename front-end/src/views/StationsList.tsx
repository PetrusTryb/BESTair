import {useEffect, useState} from "react";

export default function StationsList(){
    const [page, setPage] = useState(1);
    const [prevPage, setPrevPage] = useState(0);
    const [stations, setStations] = useState<{
        id:string,
        latitude:number,
        longitude:number,
        name:string,
        voivodeship:string
    }[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchStations = async () => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:5000/station?limit=50&offset=${(page - 1) * 50}`);
            const data = await response.json();
            //append new data to the old data
            setStations([...stations, ...data]);
            setPrevPage(page-1);
        }
        catch (e) {
            console.error(e);
        }
        finally {
            setLoading(false);
        }
    }
    useEffect(() => {
        if(prevPage === page-1){
            console.log("Page changed", prevPage, page);
            fetchStations().then(()=>setPrevPage(page));
        }
    },[page, prevPage]);
    window.onscroll = function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            setPage(page + 1);
        }
    };

return (
    <div>
        {loading ? <div className="flex justify-center items-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
        </div>:<div></div>}
        <div className="flex flex-wrap justify-center">
            {stations.map((station) => {
                return (
                    <a href={`/station?id=${station.id}`} key={station.id} className="m-2 p-2 border-2 border-gray-900 rounded-lg">
                    <div>
                        <div className="text-2xl">{station.name}</div>
                        <div className="text-xl">{station.voivodeship}</div>
                    </div>
                    </a>
                )
            })
            }
        </div>
    </div>
)
}