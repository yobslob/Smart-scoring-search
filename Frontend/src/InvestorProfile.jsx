import React from 'react';
import Select from 'react-select';

const stageOptions = [
    { value: 'Pre-seed', label: 'Pre-seed' },
    { value: 'Seed', label: 'Seed' },
    { value: 'Series A', label: 'Series A' },
    { value: 'Series B', label: 'Series B' }
];

const sectorOptions = [
    { value: 'HealthTech', label: 'HealthTech' },
    { value: 'EdTech', label: 'EdTech' },
    { value: 'FinTech', label: 'FinTech' },
    { value: 'AgriTech', label: 'AgriTech' }
];

const regionOptions = [
    { value: 'India', label: 'India' },
    { value: 'USA', label: 'USA' },
    { value: 'Europe', label: 'Europe' },
    { value: 'Asia', label: 'Asia' }
];

function InvestorProfile({ investor, onChange }) {
    return (
        <div className="border p-4 rounded shadow mb-4">
            <h2 className="text-xl font-semibold mb-2">Investor Profile</h2>
            <div className="mb-2">
                <label className="block text-sm">Name</label>
                <input
                    type="text"
                    value={investor.name}
                    onChange={(e) => onChange('name', e.target.value)}
                    placeholder="Name"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Photo URL</label>
                <input
                    type="text"
                    value={investor.photo_url}
                    onChange={(e) => onChange('photo_url', e.target.value)}
                    placeholder="Photo URL"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Designation</label>
                <input
                    type="text"
                    value={investor.designation}
                    onChange={(e) => onChange('designation', e.target.value)}
                    placeholder="Designation"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">LinkedIn</label>
                <input
                    type="text"
                    value={investor.contact_links.linkedin}
                    onChange={(e) => onChange('contact_links.linkedin', e.target.value)}
                    placeholder="LinkedIn"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Twitter</label>
                <input
                    type="text"
                    value={investor.contact_links.twitter}
                    onChange={(e) => onChange('contact_links.twitter', e.target.value)}
                    placeholder="Twitter"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Website</label>
                <input
                    type="text"
                    value={investor.contact_links.website}
                    onChange={(e) => onChange('contact_links.website', e.target.value)}
                    placeholder="Website"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Bio</label>
                <textarea
                    value={investor.bio}
                    onChange={(e) => onChange('bio', e.target.value)}
                    placeholder="Bio"
                    className="w-full border p-2 rounded"
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Stage Preference</label>
                <Select
                    isMulti
                    options={stageOptions}
                    value={investor.stage_preference.map((s) => ({ label: s, value: s }))}
                    onChange={(selected) => onChange('stage_preference', selected ? selected.map((s) => s.value) : [])}
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Sector Focus</label>
                <Select
                    isMulti
                    options={sectorOptions}
                    value={investor.sector_focus.map((s) => ({ label: s, value: s }))}
                    onChange={(selected) => onChange('sector_focus', selected ? selected.map((s) => s.value) : [])}
                />
            </div>
            <div className="mb-2">
                <label className="block text-sm">Regions Preferred</label>
                <Select
                    isMulti
                    options={regionOptions}
                    value={investor.regions_preferred.map((s) => ({ label: s, value: s }))}
                    onChange={(selected) => onChange('regions_preferred', selected ? selected.map((s) => s.value) : [])}
                />
            </div>
        </div>
    );
}

export default InvestorProfile;