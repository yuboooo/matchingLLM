import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);

  const onFileChange = event => {
    setFile(event.target.files[0]);  // Set the selected file into state
  };

  const onFileUpload = () => {
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append("file", file);  // Append the file captured from input

    axios.post("http://127.0.0.1:5000/upload", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'  // Ensure correct content-type header
      }
    })
    .then(response => alert('File uploaded successfully'))
    .catch(error => {
      console.error('Upload error:', error);
      alert('Error uploading file: ' + (error.response?.data || error.message));
    });
  };

  return (
    <div>
      <h2>File Upload</h2>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload} disabled={!file}>
        Upload!
      </button>
      {file && <p>File ready to upload: {file.name}</p>} 
    </div>
  );
}

export default FileUpload;
