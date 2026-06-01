import React, { useState, useEffect } from 'react'
import LiveMap from './components/LiveMap'
import FlightPanel from './components/FlightPanel'
import SearchBar from './components/SearchBar'
import MetricsBar from './components/MetricsBar'
import './index.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const OPEN_SKY_URL = 'https://opensky-network.org/api/states/all?lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0'

function App() {
  const [flights, setFlights] = useState([])
  const [selectedFlight, setSelectedFlight] = useState(null)
  const [loading, setLoading] = useState(false)
  const [conflicts, setConflicts] = useState(0)
  const [searchTerm, setSearchTerm] = useState('')
  const [summary, setSummary] = useState('Live flight briefing is loading...')
  const [dataSource, setDataSource] = useState(API_BASE_URL ? 'AeroShield backend' : 'OpenSky public API')

  useEffect(() => {
    const fetchFlights = async () => {
      setLoading(true)
      try {
        const url = API_BASE_URL ? `${API_BASE_URL}/api/flights` : OPEN_SKY_URL
        const response = await fetch(url)
        const data = await response.json()

        if (data.flights) {
              setFlights(data.flights)
          setConflicts(data.conflictCount || 0)
          setSummary(data.summary || 'Live flight tracking is active. No summary available.')
          setDataSource(API_BASE_URL ? 'AeroShield backend' : 'OpenSky public API')
        } else if (data.states) {
          const flightList = data.states
            .map(state => ({
              icao24: state[0],
              callsign: state[1]?.trim() || 'UNKNOWN',
              origin_country: state[2] || 'Unknown',
              latitude: state[6],
              longitude: state[5],
              altitude: state[7],
              velocity: state[9],
              heading: state[10],
              vertical_rate: state[11],
              squawk: state[14],
              timestamp: data.time
            }))
            .filter(f => f.latitude && f.longitude)

          setFlights(flightList)
          setConflicts(0)
          setSummary('Live flight tracking enabled with direct OpenSky data.')
          setDataSource('OpenSky public API')
        }
      } catch (error) {
        console.error('Backend fetch failed, falling back to OpenSky:', error)

        try {
          const fallbackResponse = await fetch(OPEN_SKY_URL)
          const fallbackData = await fallbackResponse.json()

          if (fallbackData.states) {
            const flightList = fallbackData.states
              .map(state => ({
                icao24: state[0],
                callsign: state[1]?.trim() || 'UNKNOWN',
                origin_country: state[2] || 'Unknown',
                latitude: state[6],
                longitude: state[5],
                altitude: state[7],
                velocity: state[9],
                heading: state[10],
                vertical_rate: state[11],
                squawk: state[14],
                timestamp: fallbackData.time
              }))
              .filter(f => f.latitude && f.longitude)

            setFlights(flightList)
            setConflicts(0)
            setSummary('Live flight tracking enabled with direct OpenSky data.')
            setDataSource('OpenSky public API')
            return
          }
        } catch (fallbackError) {
          console.error('OpenSky fallback also failed:', fallbackError)
        }

        setSummary('Unable to reach live data. Check the backend or network connection.')
      } finally {
        setLoading(false)
      }
    }

    fetchFlights()
    const interval = setInterval(fetchFlights, 10000)
    return () => clearInterval(interval)
  }, [])

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
