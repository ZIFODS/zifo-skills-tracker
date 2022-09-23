import GraphVis from './Graph';
import graphData from "./data/skills_js.json"

function App() {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
      }}
    >
      <GraphVis graph={graphData}/>
    </div>
  );
}

export default App;
