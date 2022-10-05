import React from 'react'
import GraphVis from "./components/graph/graph"

function App(): JSX.Element {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
      }}
    >
      <GraphVis/>
    </div>
  );
}

export default App;
