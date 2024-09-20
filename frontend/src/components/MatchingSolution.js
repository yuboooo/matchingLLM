import React, { useState } from 'react';
import axios from 'axios';

function MatchingSolution() {
    const [matchingSolution, setMatchingSolution] = useState('');  // Use camelCase for variable

    const fetchMatchingSolution = () => {
        axios.get('http://127.0.0.1:5000/matching-solution')
            .then(response => {
                setMatchingSolution(response.data.matchingSolution);  // Use camelCase and ensure it matches what the backend sends
            })
            .catch(error => {
                console.error('Error fetching matching solution:', error);
                alert('Failed to fetch matching solution');
            });
    };

    return (
        <div>
            <h2>Matching Solution</h2>
            <button onClick={fetchMatchingSolution}>Calculate Matching Solution</button>
            {matchingSolution && <p>{matchingSolution}</p>}
        </div>
    );
}

export default MatchingSolution;
