import React, { useState, useEffect } from 'react'
import LiveMap from './components/LiveMap'
import FlightPanel from './components/FlightPanel'
import SearchBar from './components/SearchBar'
import MetricsBar from './components/MetricsBar'
import './index.css'

function App() {
  const [flights, setFlights] = useState([])
  const [selectedFlight, setSelectedFlight] = useState(null)
  const [loading, setLoading] = useState(false)
  const [conflicts, setConflicts] = useState([])
  const [searchTerm, setSearchTerm] = useState('')

  // Fetch live flight data from OpenSky API
  useEffect(() => {
    const fetchFlights = async () => {
      setLoading(true)
      try {
        // JFK/NY Airspace boundary (you can change this to any region)
        const response = await fetch(
          'https://opensky-network.org/api/states/all?lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0'
        );
        
        const data = await response.json()
        
        if (data.states) {
          const flightList = data.states.map(state => ({
            icao24: state[0],
            callsign: state[1]?.trim() || 'UNKNOWN',
            origin_country: state[2],
            latitude: state[6],
            longitude: state[5],
            altitude: state[7],
            velocity: state[9],
            heading: state[10],
            vertical_rate: state[11],
            squawk: state[14],
            timestamp: data.time
          })).filter(f => f.latitude && f.longitude)
          
          setFlights(flightList)
        }
      } catch (error) {
        console.error('Error fetching flights:', error)
      } finally {
        setLoading(false)
      }
    }

    // Initial fetch
    fetchFlights()

    // Refresh every 10 seconds
    const interval = setInterval(fetchFlights, 10000)
    return () => clearInterval(interval)
  }, [])

  // Filter flights by search term
  const filteredFlights = flights.filter(f =>
    f.callsign.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.icao24.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.origin_country.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="app-container bg-dark-900 text-white min-h-screen">
      {/* Header */}
      <header className="bg-dark-700 border-b border-dark-600 p-4 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-cyan-400 mb-2">
            ✈️ AeroShield Live Tracking
          </h1>
          <p className="text-gray-400">Real-time aircraft monitoring & conflict detection</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto p-4">
        {/* Metrics */}
        <MetricsBar 
          totalFlights={filteredFlights.length}
          conflicts={conflicts.length}
          loading={loading}
        />

        {/* Search */}
        <SearchBar value={searchTerm} onChange={setSearchTerm} />

        {/* Map and Panel Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
          {/* Map (2/3 width) */}
          <div className="lg:col-span-2">
            <LiveMap 
              flights={filteredFlights}
              selectedFlight={selectedFlight}
              onFlightSelect={setSelectedFlight}
            />
          </div>

          {/* Flight Details Panel (1/3 width) */}
          <div className="lg:col-span-1">
            <FlightPanel 
              flight={selectedFlight}
              flights={filteredFlights}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
