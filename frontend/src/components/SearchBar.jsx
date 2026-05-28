import React from 'react'

const SearchBar = ({ value, onChange }) => {
  return (
    <div className="bg-dark-700 rounded-lg p-4 border border-dark-600 mt-4">
      <div className="flex items-center gap-2">
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Search by callsign, ICAO, or country..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1 bg-dark-800 border border-dark-600 rounded px-3 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500"
        />
        {value && (
          <button
            onClick={() => onChange('')}
            className="text-gray-400 hover:text-gray-300"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  )
}

export default SearchBar
