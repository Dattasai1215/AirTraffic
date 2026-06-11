// API base configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const OPEN_SKY_URL = 'https://opensky-network.org/api/states/all?lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0'

/**
 * Fetch flights from the AeroShield backend API.
 * Returns { flights, conflictCount, summary, dataSource } or throws.
 */
export async function fetchFlightsFromBackend() {
  const response = await fetch(`${API_BASE_URL}/api/flights`)
  const data = await response.json()

  if (data.flights) {
    return {
      flights: data.flights,
      conflictCount: data.conflictCount || 0,
      summary: data.summary || 'Live flight tracking is active. No summary available.',
      dataSource: 'AeroShield backend',
    }
  }

  // Backend returned OpenSky-style states array
  if (data.states) {
    const flights = data.states
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
        timestamp: data.time,
      }))
      .filter(f => f.latitude && f.longitude)

    return {
      flights,
      conflictCount: 0,
      summary: 'Live flight tracking enabled with direct OpenSky data.',
      dataSource: 'OpenSky public API',
    }
  }

  throw new Error('Unexpected response format from backend')
}

/**
 * Fetch flights directly from OpenSky Network public API (fallback).
 * Returns { flights, conflictCount, summary, dataSource } or throws.
 */
export async function fetchFlightsFromOpenSky() {
  const response = await fetch(OPEN_SKY_URL)
  const data = await response.json()

  if (!data.states) throw new Error('No states in OpenSky response')

  const flights = data.states
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
      timestamp: data.time,
    }))
    .filter(f => f.latitude && f.longitude)

  return {
    flights,
    conflictCount: 0,
    summary: 'Live flight tracking enabled with direct OpenSky data.',
    dataSource: 'OpenSky public API',
  }
}

export { API_BASE_URL, OPEN_SKY_URL }
