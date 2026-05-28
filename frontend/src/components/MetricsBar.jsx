import React from 'react'

const MetricsBar = ({ totalFlights, conflicts, loading }) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Total Flights */}
      <div className="bg-dark-700 rounded-lg p-4 border border-dark-600">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-xs uppercase tracking-wider">Surveillance Fleet</p>
            <p className={`text-3xl font-bold mt-1 ${loading ? 'text-gray-500 animate-pulse' : 'text-cyan-400'}`}>
              {totalFlights}
            </p>
          </div>
          <svg className="w-8 h-8 text-cyan-400 opacity-20" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5.951-1.429 5.951 1.429a1 1 0 001.169-1.409l-7-14z" />
          </svg>
        </div>
      </div>

      {/* Conflicts Detected */}
      <div className={`${conflicts > 0 ? 'bg-red-500/20 border-red-500' : 'bg-dark-700 border-dark-600'} rounded-lg p-4 border`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-xs uppercase tracking-wider">Conflicts</p>
            <p className={`text-3xl font-bold mt-1 ${conflicts > 0 ? 'text-red-400' : 'text-green-400'}`}>
              {conflicts}
            </p>
          </div>
          <svg className={`w-8 h-8 ${conflicts > 0 ? 'text-red-400' : 'text-green-400'} opacity-20`} fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M13.477 14.89A6 6 0 015.11 2.513a6 6 0 008.367 12.377z" clipRule="evenodd" />
          </svg>
        </div>
      </div>

      {/* API Status */}
      <div className="bg-dark-700 rounded-lg p-4 border border-dark-600">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-xs uppercase tracking-wider">Data Status</p>
            <div className="flex items-center gap-2 mt-1">
              <div className={`w-3 h-3 rounded-full ${loading ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'}`}></div>
              <p className={`text-sm font-semibold ${loading ? 'text-yellow-400' : 'text-green-400'}`}>
                {loading ? 'Updating...' : 'Live'}
              </p>
            </div>
          </div>
          <svg className="w-8 h-8 text-green-400 opacity-20" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 3.062v6.072A3.066 3.066 0 0117.853 15a4.582 4.582 0 01-1.497 3.573 4.584 4.584 0 01-5.011 0A4.582 4.582 0 017 15a3.066 3.066 0 01-3.066-3.066V6.517a3.066 3.066 0 012.812-3.062zM9 12a1 1 0 11-2 0 1 1 0 012 0z" clipRule="evenodd" />
          </svg>
        </div>
      </div>
    </div>
  )
}

export default MetricsBar
