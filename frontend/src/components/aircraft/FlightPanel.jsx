import React from 'react'

const FlightPanel = ({ flight, flights }) => {
  if (!flight) {
    return (
      <div className="bg-dark-700 rounded-lg p-6 border border-dark-600 h-96 flex items-center justify-center">
        <div className="text-center text-gray-400">
          <p className="text-lg">Click an aircraft on map</p>
          <p className="text-sm mt-2">to view details</p>
          <p className="text-xs mt-4 text-gray-500">
            {flights.length} aircraft tracked
          </p>
        </div>
      </div>
    )
  }

  const altitude = flight.altitude ? (flight.altitude / 100).toFixed(0) : 'N/A'
  const speed = flight.velocity ? (flight.velocity * 1.944).toFixed(0) : 'N/A'
  const vspeed = flight.vertical_rate ? (flight.vertical_rate * 196.85).toFixed(0) : 'N/A'

  return (
    <div className="bg-dark-700 rounded-lg p-6 border border-dark-600 h-96 overflow-y-auto">
      {/* Header */}
      <div className="mb-6 pb-4 border-b border-dark-600">
        <h2 className="text-2xl font-bold text-cyan-400 mb-1">
          {flight.callsign}
        </h2>
        <p className="text-xs text-gray-400">{flight.icao24}</p>
      </div>

      {/* Flight Details */}
      <div className="space-y-4 text-sm">
        {/* Position */}
        <div className="bg-dark-800/50 p-3 rounded">
          <p className="text-gray-400 text-xs uppercase">Position</p>
          <p className="text-green-400 font-mono">
            {flight.latitude.toFixed(4)}°, {flight.longitude.toFixed(4)}°
          </p>
        </div>

        {/* Altitude */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-dark-800/50 p-3 rounded">
            <p className="text-gray-400 text-xs uppercase">Altitude</p>
            <p className="text-blue-400 font-mono text-lg">{altitude}00 ft</p>
          </div>
          <div className="bg-dark-800/50 p-3 rounded">
            <p className="text-gray-400 text-xs uppercase">V/Speed</p>
            <p className={`font-mono text-lg ${vspeed > 0 ? 'text-red-400' : vspeed < 0 ? 'text-green-400' : 'text-gray-400'}`}>
              {vspeed} ft/m
            </p>
          </div>
        </div>

        {/* Speed & Heading */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-dark-800/50 p-3 rounded">
            <p className="text-gray-400 text-xs uppercase">Ground Spd</p>
            <p className="text-orange-400 font-mono text-lg">{speed} kt</p>
          </div>
          <div className="bg-dark-800/50 p-3 rounded">
            <p className="text-gray-400 text-xs uppercase">Heading</p>
            <p className="text-purple-400 font-mono text-lg">{flight.heading || 'N/A'}°</p>
          </div>
        </div>

        {/* Country & Squawk */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-dark-800/50 p-3 rounded">
            <p className="text-gray-400 text-xs uppercase">Country</p>
            <p className="text-white font-semibold">{flight.origin_country}</p>
          </div>
          <div className="bg-dark-800/50 p-3 rounded">
            <p className="text-gray-400 text-xs uppercase">Squawk</p>
            <p className="text-white font-mono">{flight.squawk || 'N/A'}</p>
          </div>
        </div>

        {/* Data Quality */}
        <div className="bg-dark-800/50 p-3 rounded text-xs">
          <p className="text-gray-400 uppercase">Data Quality</p>
          <div className="mt-2 flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <p className="text-green-400">Live tracking active</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FlightPanel
