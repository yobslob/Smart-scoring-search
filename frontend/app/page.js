"use client";
import { useState } from 'react';
import Select from 'react-select';
import { motion, AnimatePresence } from 'framer-motion';

export default function Home() {
  const [keyword, setKeyword] = useState('');
  const [selectedStages, setSelectedStages] = useState([]);
  const [selectedSectors, setSelectedSectors] = useState([]);
  const [selectedRegions, setSelectedRegions] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const stageOptions = [
    { value: 'Pre-seed', label: 'Pre-seed' },
    { value: 'Seed', label: 'Seed' },
    { value: 'Series A', label: 'Series A' },
    { value: 'Series B', label: 'Series B' },
    { value: 'Growth', label: 'Growth' },
  ];

  const sectorOptions = [
    { value: 'FinTech', label: 'FinTech' },
    { value: 'SaaS', label: 'SaaS' },
    { value: 'HealthTech', label: 'HealthTech' },
    { value: 'EdTech', label: 'EdTech' },
    { value: 'E-commerce', label: 'E-commerce' },
    { value: 'AI', label: 'AI' },
    { value: 'Blockchain', label: 'Blockchain' },
  ];

  const regionOptions = [
    { value: 'India', label: 'India' },
    { value: 'USA', label: 'USA' },
    { value: 'Europe', label: 'Europe' },
    { value: 'Asia', label: 'Asia' },
    { value: 'Africa', label: 'Africa' },
  ];

  const handleSearch = async () => {
    setLoading(true);
    const response = await fetch('http://localhost:8000/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        keyword: keyword,
        stage_preferences: selectedStages.map(option => option.value),
        sector_focus: selectedSectors.map(option => option.value),
        regions_preferred: selectedRegions.map(option => option.value),
      })
    });
    const data = await response.json();

    if (response.ok && Array.isArray(data)) {
      setResults(data);
    } else {
      console.error("Error from server:", data.detail);
      setResults([]);
    }

    setLoading(false);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">SEARCH ENGINE</h1>
      <div className="flex justify-center mb-4">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Enter keyword"
          className="border p-2 mr-2 rounded w-64"
        />
        <button onClick={handleSearch} className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
          Search
        </button>
      </div>
      <div className="max-w-3xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 text-emerald-800 ">
        <Select
          instanceId="stage-select"
          isMulti
          options={stageOptions}
          value={selectedStages}
          onChange={setSelectedStages}
          placeholder="Select stage preferences"
          className="w-full"
        />
        <Select
          instanceId="sector-select"
          isMulti
          options={sectorOptions}
          value={selectedSectors}
          onChange={setSelectedSectors}
          placeholder="Select sector focus"
          className="w-full"
        />
        <Select
          instanceId="region-select"
          isMulti
          options={regionOptions}
          value={selectedRegions}
          onChange={setSelectedRegions}
          placeholder="Select regions preferred"
          className="w-full"
        />
      </div>
      {loading && <p className="text-center text-gray-500">Loading...</p>}
      <div className="max-w-6xl mx-auto space-y-4">
        {results.length === 0 && !loading && (
          <p className="text-center text-gray-500">No startups found.</p>
        )}
        <AnimatePresence>
          {results.map((startup, index) => (
            <motion.div
              key={startup.startup_name + index}
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="bg-blue-100 shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow"
            >
              <h2 className="text-xl font-semibold text-gray-800">{startup.startup_name}</h2>
              <p className="text-gray-600">Score: {startup.score}</p>
              <p className="text-gray-600">
                Industry: {startup.industry} | Stage: {startup.stage} | Region: {startup.region}
              </p>
              <p className="text-gray-500 italic">{startup.tagline}</p>
              <a
                href={startup.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline"
              >
                Website
              </a>
            </motion.div>
          ))}
        </AnimatePresence>

      </div>
    </div>
  );
}