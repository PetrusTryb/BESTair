import React from 'react';
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import './App.css';
import Navbar from "./components/Navbar";
import Map from "./views/Map";
import StationsList from "./views/StationsList";
import StationDetails from "./views/StationDetails";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
          <Navbar/>
          <Routes>
                <Route path="/" element={<Map/>}/>
                <Route path="/stations" element={<StationsList/>}/>
                <Route path="/station" element={<StationDetails/>}/>
          </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
