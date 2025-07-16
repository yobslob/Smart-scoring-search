import React from 'react';

function StartupList({ startups }) {
    return (
        <div className="mt-4">
            <h2 className="text-xl font-semibold mb-2">Matching Startups</h2>
            {startups.length === 0 && <p>No startups found.</p>}
            {startups.map((startup, index) => (
                <div key={index} className="border p-4 rounded shadow mb-2">
                    <h3 className="text-lg font-bold">{startup.startup_name}</h3>
                    <p><strong>Score:</strong> {startup.score}</p>
                    <p><strong>Website:</strong> <a href={startup.website} target="_blank" rel="noopener noreferrer">{startup.website}</a></p>
                    <p><strong>Tagline:</strong> {startup.tagline}</p>
                    <p><strong>Profile:</strong></p>
                    <pre className="whitespace-pre-wrap">{startup.profile}</pre>
                </div>
            ))}
        </div>
    );
}

export default StartupList;