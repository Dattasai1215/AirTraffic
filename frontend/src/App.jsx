import React, { useState } from 'react'
import LiveMap from './components/maps/LiveMap'
import FlightPanel from './components/aircraft/FlightPanel'
import SearchBar from './components/SearchBar'
import MetricsBar from './components/charts/MetricsBar'
import { useFlights } from './hooks/useFlights'
import './styles/index.css'

function App() {
  const [selectedFlight, setSelectedFlight] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  const { flights, conflicts, loading, summary, dataSource } = useFlights()

  const filteredFlights = flights.filter(f =>
    f.callsign.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.icao24.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.origin_country.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="app-container bg-dark-900 text-white min-h-screen">
      <header className="bg-dark-700 border-b border-dark-600 p-4 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-cyan-400 mb-2">
            ✈️ AeroShield Live Tracking
          </h1>
          <p className="text-gray-400">Real-time aircraft monitoring, ML prediction, and AI alerts.</p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-4">
        <div className="grid gap-4 lg:grid-cols-[2fr_1fr]">
          <MetricsBar
            totalFlights={filteredFlights.length}
            conflicts={conflicts}
            loading={loading}
          />

          <div className="bg-dark-700 rounded-lg border border-dark-600 p-4 text-sm text-gray-200">
            <div className="flex items-center justify-between mb-3 gap-3">
              <div>
                <p className="text-gray-400 uppercase text-xs tracking-wider">AI Summary</p>
                <p className="text-white font-semibold text-lg mt-1">Live briefing</p>
              </div>
              <span className="text-xs text-cyan-300">{dataSource}</span>
            </div>
            <p className="leading-6">{summary}</p>
          </div>
        </div>

        <SearchBar value={searchTerm} onChange={setSearchTerm} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
          <div className="lg:col-span-2">
            <LiveMap
              flights={filteredFlights}
              selectedFlight={selectedFlight}
              onFlightSelect={setSelectedFlight}
            />
          </div>

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
