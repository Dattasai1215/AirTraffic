import { useState, useEffect } from 'react'
import { fetchFlightsFromBackend, fetchFlightsFromOpenSky } from '../api/flightsApi'

/**
 * Custom hook that manages live flight data fetching with automatic
 * refresh every 10 seconds and fallback to OpenSky public API.
 *
 * @returns {{ flights, conflicts, loading, summary, dataSource }}
 */
export function useFlights() {
  const [flights, setFlights] = useState([])
  const [conflicts, setConflicts] = useState(0)
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState('Live flight briefing is loading...')
  const [dataSource, setDataSource] = useState('AeroShield backend')

  useEffect(() => {
    const fetchFlights = async () => {
      setLoading(true)
      try {
        const result = await fetchFlightsFromBackend()
        setFlights(result.flights)
        setConflicts(result.conflictCount)
        setSummary(result.summary)
        setDataSource(result.dataSource)
      } catch (error) {
        console.error('Backend fetch failed, falling back to OpenSky:', error)

        try {
          const fallback = await fetchFlightsFromOpenSky()
          setFlights(fallback.flights)
          setConflicts(fallback.conflictCount)
          setSummary(fallback.summary)
          setDataSource(fallback.dataSource)
        } catch (fallbackError) {
          console.error('OpenSky fallback also failed:', fallbackError)
          setSummary('Unable to reach live data. Check the backend or network connection.')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchFlights()
    const interval = setInterval(fetchFlights, 10000)
    return () => clearInterval(interval)
  }, [])

  return { flights, conflicts, loading, summary, dataSource }
}
