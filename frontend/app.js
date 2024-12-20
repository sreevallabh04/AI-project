import React, { useState } from 'react';

function App() {
  const [command, setCommand] = useState('');
  const [response, setResponse] = useState('');

  const handleCommand = async () => {
    const res = await fetch('/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Virtual Assistant</h1>
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Type your command..."
        style={{ padding: '10px', width: '80%' }}
      />
      <button onClick={handleCommand} style={{ padding: '10px' }}>
        Send
      </button>
      <div style={{ marginTop: '20px' }}>
        <strong>Response:</strong> <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
