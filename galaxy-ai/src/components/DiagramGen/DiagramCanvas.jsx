import React, { useState, useRef } from 'react';
import DiagramControls from './DiagramControls';
import { Network, Trash2, Edit3, Move, Layers } from 'lucide-react';

export default function DiagramCanvas() {
  const [layoutType, setLayoutType] = useState('mindmap'); // 'mindmap', 'workflow', 'system'

  // Default Presets
  const presets = {
    mindmap: {
      nodes: [
        { id: '1', title: 'Galaxy AI Core', desc: 'Central Operating Engine', x: 420, y: 160, color: '#00F0FF' },
        { id: '2', title: 'Local SQLite DB', desc: 'Zero-cloud persistent storage', x: 180, y: 80, color: '#7000FF' },
        { id: '3', title: 'Voice & Soul Engine', desc: 'Acoustic waveform & personality tuner', x: 660, y: 80, color: '#EC4899' },
        { id: '4', title: 'Agent Town', desc: '4 Virtual Specialists', x: 180, y: 260, color: '#10B981' },
        { id: '5', title: 'Android Companion', desc: 'Mobile Voice & File analyzer', x: 660, y: 260, color: '#F59E0B' },
      ],
      edges: [
        { from: '1', to: '2' },
        { from: '1', to: '3' },
        { from: '1', to: '4' },
        { from: '1', to: '5' },
      ],
    },
    workflow: {
      nodes: [
        { id: '1', title: 'User Vocal Directive', desc: '"Open file manager & send photos"', x: 120, y: 180, color: '#00F0FF' },
        { id: '2', title: 'NLP Intent Extractor', desc: 'Extracts drive, folder, contact', x: 380, y: 180, color: '#7000FF' },
        { id: '3', title: 'OS Automator (D:\\)', desc: 'Scans images & sets clipboard', x: 640, y: 120, color: '#10B981' },
        { id: '4', title: 'WhatsApp Bridge', desc: 'Pastes media & clicks send', x: 900, y: 180, color: '#EC4899' },
      ],
      edges: [
        { from: '1', to: '2' },
        { from: '2', to: '3' },
        { from: '3', to: '4' },
      ],
    },
    system: {
      nodes: [
        { id: '1', title: 'Electron Main (Node.js)', desc: 'IPC, DB & OS bridge', x: 200, y: 120, color: '#7000FF' },
        { id: '2', title: 'React 18 Renderer', desc: 'Tailwind Cyberpunk UI', x: 200, y: 280, color: '#00F0FF' },
        { id: '3', title: 'better-sqlite3 Engine', desc: 'Local memory & telemetry logs', x: 520, y: 120, color: '#10B981' },
        { id: '4', title: 'OS Child Processes', desc: 'Photoshop, Explorer, Calc', x: 520, y: 280, color: '#F59E0B' },
        { id: '5', title: 'Android React Native', desc: 'WebSocket/IPC companion', x: 840, y: 200, color: '#EC4899' },
      ],
      edges: [
        { from: '1', to: '2' },
        { from: '1', to: '3' },
        { from: '1', to: '4' },
        { from: '1', to: '5' },
      ],
    },
  };

  const [currentDiagram, setCurrentDiagram] = useState(presets[layoutType]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [draggingNodeId, setDraggingNodeId] = useState(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

  const containerRef = useRef(null);

  // Switch layout preset
  const handleLayoutChange = (type) => {
    setLayoutType(type);
    setCurrentDiagram(presets[type] || presets.mindmap);
    setSelectedNodeId(null);
  };

  // Node Dragging
  const handleMouseDown = (e, nodeId) => {
    e.stopPropagation();
    setSelectedNodeId(nodeId);
    setDraggingNodeId(nodeId);

    const node = currentDiagram.nodes.find((n) => n.id === nodeId);
    if (node) {
      setDragOffset({
        x: e.clientX - node.x,
        y: e.clientY - node.y,
      });
    }
  };

  const handleMouseMove = (e) => {
    if (!draggingNodeId) return;

    setCurrentDiagram((prev) => ({
      ...prev,
      nodes: prev.nodes.map((node) => {
        if (node.id === draggingNodeId) {
          return {
            ...node,
            x: Math.max(20, Math.min(1100, e.clientX - dragOffset.x)),
            y: Math.max(20, Math.min(500, e.clientY - dragOffset.y)),
          };
        }
        return node;
      }),
    }));
  };

  const handleMouseUp = () => {
    setDraggingNodeId(null);
  };

  // Add new node
  const handleAddNode = () => {
    const newId = String(Date.now());
    const colors = ['#00F0FF', '#7000FF', '#EC4899', '#10B981', '#F59E0B'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];

    const newNode = {
      id: newId,
      title: `New Component ${currentDiagram.nodes.length + 1}`,
      desc: 'Configurable node descriptor',
      x: 350 + Math.random() * 100,
      y: 180 + Math.random() * 80,
      color: randomColor,
    };

    setCurrentDiagram((prev) => ({
      nodes: [...prev.nodes, newNode],
      edges: prev.nodes.length > 0 ? [...prev.edges, { from: prev.nodes[0].id, to: newId }] : prev.edges,
    }));
    setSelectedNodeId(newId);
  };

  // Delete node
  const handleDeleteNode = (id) => {
    setCurrentDiagram((prev) => ({
      nodes: prev.nodes.filter((n) => n.id !== id),
      edges: prev.edges.filter((e) => e.from !== id && e.to !== id),
    }));
    if (selectedNodeId === id) setSelectedNodeId(null);
  };

  // Generate from Prompt
  const handleGenerateFromPrompt = (prompt, type) => {
    const generatedNodes = [
      { id: '1', title: `${prompt} Core`, desc: 'Root Architecture', x: 200, y: 200, color: '#00F0FF' },
      { id: '2', title: 'Data Ingestion Layer', desc: 'Real-time telemetry stream', x: 480, y: 100, color: '#7000FF' },
      { id: '3', title: 'Processing & Indexing', desc: 'SQLite Vector + Structured table', x: 480, y: 300, color: '#10B981' },
      { id: '4', title: 'Action Dispatcher', desc: 'OS & Voice response synthesis', x: 780, y: 200, color: '#EC4899' },
    ];
    const generatedEdges = [
      { from: '1', to: '2' },
      { from: '2', to: '3' },
      { from: '3', to: '4' },
    ];

    setCurrentDiagram({ nodes: generatedNodes, edges: generatedEdges });
  };

  // Export JSON
  const handleExport = () => {
    const jsonStr = JSON.stringify(currentDiagram, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `galaxy-diagram-${layoutType}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-full flex flex-col p-6 space-y-4 overflow-hidden select-none">
      {/* Top Controls */}
      <DiagramControls
        layoutType={layoutType}
        setLayoutType={handleLayoutChange}
        onAddNode={handleAddNode}
        onGenerateFromPrompt={handleGenerateFromPrompt}
        onResetLayout={() => setCurrentDiagram(presets[layoutType])}
        onExport={handleExport}
      />

      {/* Interactive Visual Canvas */}
      <div
        ref={containerRef}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onClick={() => setSelectedNodeId(null)}
        className="flex-1 bg-void-card/70 border border-slate-800/80 rounded-2xl relative overflow-hidden cyber-grid shadow-inner cursor-crosshair min-h-[460px]"
      >
        {/* SVG Curved Connections */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
          <defs>
            <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#7000FF" stopOpacity="0.7" />
            </linearGradient>
          </defs>
          {currentDiagram.edges.map((edge, idx) => {
            const fromNode = currentDiagram.nodes.find((n) => n.id === edge.from);
            const toNode = currentDiagram.nodes.find((n) => n.id === edge.to);
            if (!fromNode || !toNode) return null;

            // Draw smooth bezier curve between node centers
            const x1 = fromNode.x + 100;
            const y1 = fromNode.y + 40;
            const x2 = toNode.x + 100;
            const y2 = toNode.y + 40;
            const cx = (x1 + x2) / 2;

            return (
              <g key={idx}>
                <path
                  d={`M ${x1} ${y1} C ${cx} ${y1}, ${cx} ${y2}, ${x2} ${y2}`}
                  stroke="url(#edgeGrad)"
                  strokeWidth="2"
                  fill="none"
                  strokeDasharray="4 2"
                />
                <circle cx={x2} cy={y2} r="4" fill="#00F0FF" />
              </g>
            );
          })}
        </svg>

        {/* Draggable Diagram Nodes */}
        {currentDiagram.nodes.map((node) => {
          const isSelected = selectedNodeId === node.id;
          return (
            <div
              key={node.id}
              onMouseDown={(e) => handleMouseDown(e, node.id)}
              style={{
                left: `${node.x}px`,
                top: `${node.y}px`,
                borderColor: isSelected ? node.color : `${node.color}55`,
              }}
              className={`absolute w-52 p-3.5 rounded-xl bg-void-light/95 border backdrop-blur-md cursor-grab active:cursor-grabbing transition-shadow z-10 ${
                isSelected ? 'shadow-2xl scale-[1.03] ring-1 ring-cyan-neon' : 'hover:border-slate-600'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span
                  className="w-2.5 h-2.5 rounded-full"
                  style={{ backgroundColor: node.color }}
                />
                <div className="flex items-center space-x-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      const newTitle = prompt('Edit Node Title:', node.title);
                      if (newTitle) {
                        setCurrentDiagram((prev) => ({
                          ...prev,
                          nodes: prev.nodes.map((n) => (n.id === node.id ? { ...n, title: newTitle } : n)),
                        }));
                      }
                    }}
                    className="p-1 rounded text-slate-500 hover:text-slate-200"
                  >
                    <Edit3 className="w-3 h-3" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteNode(node.id);
                    }}
                    className="p-1 rounded text-slate-500 hover:text-red-400"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              </div>

              <h4 className="text-xs font-bold font-mono text-slate-100 truncate">{node.title}</h4>
              <p className="text-[10px] text-slate-400 font-sans mt-0.5 line-clamp-2">{node.desc}</p>
            </div>
          );
        })}

        {/* Canvas HUD Legend */}
        <div className="absolute bottom-3 right-4 z-20 text-[10px] font-mono text-slate-400 bg-void/80 px-3 py-1.5 rounded-lg border border-slate-800 backdrop-blur-md flex items-center space-x-4">
          <span>Nodes: {currentDiagram.nodes.length}</span>
          <span>Connections: {currentDiagram.edges.length}</span>
          <span>Drag nodes freely to rearrange</span>
        </div>
      </div>
    </div>
  );
}

