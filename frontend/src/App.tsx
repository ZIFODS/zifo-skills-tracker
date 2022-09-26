import React from 'react'
import GraphVis from "./components/graph/Graph"
import graphData from "./data/d3_skills.json"

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
      <GraphVis data={graphData}/>
    </div>
  );
}

export default App;
