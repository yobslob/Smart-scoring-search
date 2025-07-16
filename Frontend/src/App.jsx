import React, { useState } from 'react';
import InvestorProfile from './InvestorProfile.jsx';
import StartupList from './StartupList.jsx';

const initialInvestor = {
  name: "Shripati Acharya",
  photo_url: "https://stellarisvp.com/wp-content/uploads/2020/03/Shripati-Dummy.jpg",
  designation: "Managing Partner at Prime Venture Partners",
  contact_links: {
    linkedin: "https://www.linkedin.com/in/shripatiacharya/",
    twitter: "https://twitter.com/shripati",
    website: "https://primevp.in/team/shripati-acharya/"
  },
  bio: "Former Silicon Valley operator turned VC. Focuses on deep relationships with founders and backing disruptive Indian startups from the early stage.",
  stage_preference: ["Pre-seed", "Seed", "Series A"],
  sector_focus: ["HealthTech"],
  regions_preferred: ["India"]
};

function App() {
  const [investor, setInvestor] = useState(initialInvestor);
  const [startups, setStartups] = useState([]);

  const handleInputChange = (field, value) => {
    setInvestor((prev) => {
      if (field.includes('.')) {
        const [parent, child] = field.split('.');
        return {
          ...prev,
          [parent]: {
            ...prev[parent],
            [child]: value
          }
        };
      } else {
        return {
          ...prev,
          [field]: value
        };
      }
    });
  };

  const handleSearch = async () => {
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(investor)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setStartups(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Startup Matcher</h1>
      <InvestorProfile investor={investor} onChange={handleInputChange} />
      <button
        onClick={handleSearch}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Search
      </button>
      <StartupList startups={startups} />
    </div>
  );
}

export default App;