import React, { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const LiveMap = ({ flights, selectedFlight, onFlightSelect }) => {
  const mapContainer = useRef(null)
  const map = useRef(null)
  const markersRef = useRef({})

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current) return

    if (!map.current) {
      map.current = L.map(mapContainer.current).setView([40.5, -73.5], 8)

      // Dark tile layer
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors © CARTO',
        minZoom: 5,
        maxZoom: 16
      }).addTo(map.current)

      // Custom pane for markers
      map.current.createPane('markers').style.zIndex = 650
    }

    return () => {
      // Cleanup
    }
  }, [])

  // Update markers
  useEffect(() => {
    if (!map.current) return

    // Remove old markers
    Object.keys(markersRef.current).forEach(icao => {
      if (!flights.find(f => f.icao24 === icao)) {
        map.current.removeLayer(markersRef.current[icao])
        delete markersRef.current[icao]
      }
    })

    // Update or create markers
    flights.forEach(flight => {
      const isSelected = selectedFlight?.icao24 === flight.icao24
      
      // Create plane icon with rotation
      const planeIcon = L.divIcon({
        className: 'plane-marker',
        html: `
          <div style="
            transform: rotate(${flight.heading || 0}deg);
            font-size: 24px;
            filter: ${isSelected ? 'drop-shadow(0 0 8px #06b6d4)' : 'drop-shadow(0 0 4px rgba(34, 211, 238, 0.5))'};
            cursor: pointer;
          ">
            ✈️
          </div>
        `,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
      })

      if (markersRef.current[flight.icao24]) {
        // Update existing marker
        markersRef.current[flight.icao24].setLatLng([flight.latitude, flight.longitude])
        markersRef.current[flight.icao24].setIcon(planeIcon)
      } else {
        // Create new marker
        const marker = L.marker(
          [flight.latitude, flight.longitude],
          { icon: planeIcon, pane: 'markers' }
        )
          .bindPopup(`
            <div class="bg-dark-700 p-3 rounded text-white">
              <b>${flight.callsign}</b><br/>
              Alt: ${(flight.altitude / 100).toFixed(0)}00 ft<br/>
              Spd: ${flight.velocity ? (flight.velocity * 1.944).toFixed(0) : 'N/A'} kt<br/>
              Hdg: ${flight.heading || 'N/A'}°<br/>
              ${flight.origin_country ? `Country: ${flight.origin_country}` : ''}
            </div>
          `)
          .on('click', () => onFlightSelect(flight))
          .addTo(map.current)

        markersRef.current[flight.icao24] = marker
      }
    })
  }, [flights, selectedFlight, onFlightSelect])

  return (
    <div className="map-wrapper">
      <div
        ref={mapContainer}
        style={{
          height: '600px',
          width: '100%',
          borderRadius: '12px',
          border: '1px solid #334155'
        }}
      />
    </div>
  )
}

export default LiveMap
