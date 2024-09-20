import React from 'react';
import Profile from './components/Profile';
import FileUpload from './components/FileUpload';
import MatchingSolution from './components/MatchingSolution';
import Chat from './components/Chat';
import './index.css';

function App() {

  return (
    <div className="App">
      <Profile />
      <FileUpload />
      <MatchingSolution />
      <Chat />
    </div>
  );
}

export default App;
