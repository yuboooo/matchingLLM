import React, { useState } from 'react';
import axios from 'axios';

function Profile() {
    const [profile, setProfile] = useState('');

    const fetchProfile = () => {
        axios.get('http://127.0.0.1:5000/generate-profile')
            .then(response => {
                // Convert the profile data to a JSON string for display
                setProfile(JSON.stringify(response.data, null, 2));  // Adding spacing for readability
            })
            .catch(error => {
                console.error('Error fetching profile:', error);
                alert('Failed to fetch profile');
            });
    };

    return (
        <div>
            <h2>Preference Profile Generator</h2>
            <button onClick={fetchProfile}>Generate Preference Profile Randomly</button>
            {/* Display the profile data as preformatted text */}
            <pre>{profile}</pre>
        </div>
    );
}

export default Profile;
