import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

function Chat() {
    const [explanation, setExplanation] = useState('');
    const [loading, setLoading] = useState(false);  // State to track loading status

    const fetchExplanation = () => {
        setLoading(true);  // Set loading to true when the fetch starts
        axios.get('http://127.0.0.1:5000/llm-explanation')
            .then(response => {
                setExplanation(response.data.explanation);
                setLoading(false);  // Set loading to false when fetching completes
            })
            .catch(error => {
                console.error('Error fetching explanation:', error);
                setExplanation('Failed to fetch explanation');
                setLoading(false);  // Ensure loading is set to false even if there is an error
            });
    };

    return (
        <div>
            <h2>Stable Matching Explanation</h2>
            <button onClick={fetchExplanation} disabled={loading}>
                {loading ? 'Loading...' : 'Start Explain'}
            </button>
            <div>
                {loading ? <p>Loading...</p> : <ReactMarkdown>{explanation}</ReactMarkdown>}
            </div>
        </div>
    );
}

export default Chat;
