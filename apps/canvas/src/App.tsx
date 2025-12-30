import { useState, useCallback } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  applyNodeChanges, 
  applyEdgeChanges, 
  Node, 
  Edge, 
  Handle, 
  Position 
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import { Film, Wand2, Play, CheckCircle } from 'lucide-react';

// Use localhost for local dev
const API_URL = "http://localhost:8000";

// --- CUSTOM NODE COMPONENTS ---

// 1. The Source Node (Input)
const SourceNode = ({ data }: any) => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleIngest = async () => {
    if (!url) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/ingest`, { url });
      data.onIngest(res.data.id); // Callback to App component
    } catch (e) {
      console.error(e);
      alert("Error ingesting video. Is Python running?");
    }
    setLoading(false);
  };

  return (
    <div className="bg-panel border-2 border-slate-700 rounded-xl p-4 w-80 shadow-2xl">
      <div className="flex items-center gap-2 mb-3 text-accent font-bold">
        <Film size={20} />
        <span>Source Material</span>
      </div>
      <input 
        type="text" 
        placeholder="YouTube URL..." 
        className="w-full bg-black/50 text-white p-2 rounded border border-slate-700 mb-2 text-sm outline-none focus:border-accent"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button 
        onClick={handleIngest}
        disabled={loading}
        className="w-full bg-accent hover:bg-blue-600 text-white p-2 rounded font-bold transition-all flex items-center justify-center gap-2"
      >
        {loading ? <Wand2 className="animate-spin" size={16} /> : <Wand2 size={16} />}
        {loading ? "Processing..." : "Ingest Video"}
      </button>
      <Handle type="source" position={Position.Right} className="bg-accent" />
    </div>
  );
};

// 2. The Clip Node (Output)
const ClipNode = ({ data }: any) => {
  const [rendering, setRendering] = useState(false);
  const [done, setDone] = useState(false);

  const handleRender = async () => {
    setRendering(true);
    try {
      await axios.post(`${API_URL}/render/${data.videoId}/${data.index}`);
      setDone(true);
    } catch (e) {
      console.error(e);
      alert("Render Failed");
    }
    setRendering(false);
  };

  return (
    <div className="bg-panel border border-slate-700 rounded-xl p-3 w-64 shadow-xl hover:border-accent transition-colors">
      <Handle type="target" position={Position.Left} className="bg-slate-500" />
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-sm text-white leading-tight">{data.title}</h3>
        <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full">
          {data.score}
        </span>
      </div>
      <p className="text-xs text-slate-400 mb-3 line-clamp-2">{data.reasoning}</p>
      
      <button 
        onClick={handleRender}
        disabled={rendering || done}
        className={`w-full p-1.5 rounded text-xs font-bold flex items-center justify-center gap-1.5 ${
          done ? "bg-green-600" : "bg-slate-700 hover:bg-slate-600"
        }`}
      >
        {done ? <CheckCircle size={14} /> : rendering ? <Wand2 className="animate-spin" size={14}/> : <Play size={14}/>}
        {done ? "Done" : rendering ? "Rendering..." : "Render Clip"}
      </button>
    </div>
  );
};

const nodeTypes = { sourceNode: SourceNode, clipNode: ClipNode };

// --- MAIN APP ---

export default function App() {
  const [nodes, setNodes] = useState<Node[]>([
    { id: '1', type: 'sourceNode', position: { x: 100, y: 100 }, data: { onIngest: (id: string) => handleAnalysis(id) } }
  ]);
  const [edges, setEdges] = useState<Edge[]>([]);

  const onNodesChange = useCallback((changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)), []);
  const onEdgesChange = useCallback((changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)), []);

  const handleAnalysis = async (videoId: string) => {
    // 1. Create a "Brain" Node to show thinking
    const brainNodeId = 'brain';
    const brainNode: Node = {
      id: brainNodeId,
      data: { label: 'Analyzing with Gemini...' },
      position: { x: 500, y: 100 },
      style: { background: '#3b82f6', color: 'white', border: 'none', padding: '10px', borderRadius: '8px', textAlign: 'center' }
    };
    
    setNodes((nds) => [...nds, brainNode]);
    setEdges((eds) => [...eds, { id: 'e1-brain', source: '1', target: brainNodeId, animated: true, style: { stroke: '#3b82f6' } }]);

    // 2. Call the AI
    try {
      const res = await axios.post(`${API_URL}/analyze/${videoId}`);
      const clips = res.data.segments;

      // 3. Remove Brain Node and Spawn Clips
      setNodes((nds) => nds.filter((n) => n.id !== brainNodeId));
      
      const newNodes: Node[] = clips.map((clip: any, index: number) => ({
        id: `clip-${index}`,
        type: 'clipNode',
        position: { x: 800, y: 50 + (index * 180) }, // Stagger them vertically
        data: { 
          title: clip.title, 
          score: clip.virality_score, 
          reasoning: clip.reasoning,
          videoId: videoId,
          index: index
        }
      }));

      const newEdges: Edge[] = clips.map((_: any, index: number) => ({
        id: `e1-clip-${index}`,
        source: '1',
        target: `clip-${index}`,
        animated: true,
        style: { stroke: '#3b82f6' }
      }));

      setNodes((nds) => [...nds, ...newNodes]);
      setEdges((eds) => [...eds, ...newEdges]);

    } catch (e) {
      console.error(e);
      // Remove brain node if fail
      setNodes((nds) => nds.filter((n) => n.id !== brainNodeId));
      alert("Analysis Failed. Check Python Console.");
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#222" gap={16} />
        <Controls className="bg-panel border-slate-700" />
      </ReactFlow>
    </div>
  );
}