import React, { useState } from 'react';
import { Network, Plus, Download, Layout, Sparkles, RefreshCw } from 'lucide-react';

export default function DiagramControls({
  layoutType,
  setLayoutType,
  onAddNode,
  onGenerateFromPrompt,
  onResetLayout,
  onExport,
}) {
  const [promptText, setPromptText] = useState('');

  const handleGenerate = (e) => {
    e.preventDefault();
    if (!promptText.trim()) return;
    onGenerateFromPrompt(promptText.trim(), layoutType);
    setPromptText('');
  };

  const layoutOptions = [
    { id: 'mindmap', label: 'Mind Map' },
    { id: 'workflow', label: 'Workflow' },
    { id: 'system', label: 'System Architecture' },
  ];

  return (
    <div className="bg-void-card border border-slate-800/80 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
      {/* Layout Type Switcher */}
      <div className="flex items-center space-x-2">
        <span className="text-[10px] font-mono text-slate-400 uppercase">Diagram Type:</span>
        <div className="flex items-center space-x-1 bg-void-light p-1 rounded-xl border border-slate-800">
          {layoutOptions.map((opt) => (
            <button
              key={opt.id}
              onClick={() => setLayoutType(opt.id)}
              className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition ${
                layoutType === opt.id
                  ? 'bg-cyan-neon/20 text-cyan-neon border border-cyan-neon/40 shadow-neon-cyan'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Prompt AI Generator Bar */}
      <form onSubmit={handleGenerate} className="flex-1 max-w-md flex items-center space-x-2">
        <input
          type="text"
          value={promptText}
          onChange={(e) => setPromptText(e.target.value)}
          placeholder={`Describe a ${layoutType} to generate (e.g. "Microservices auth flow")...`}
          className="flex-1 bg-void-light border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 font-mono focus:outline-none focus:border-cyan-neon"
        />
        <button
          type="submit"
          className="flex items-center space-x-1 bg-gradient-to-r from-cyan-neon to-purple-electric hover:opacity-90 text-void font-bold text-xs px-3.5 py-1.5 rounded-xl transition shadow-neon-cyan"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Generate</span>
        </button>
      </form>

      {/* Action Buttons */}
      <div className="flex items-center space-x-2">
        <button
          onClick={onAddNode}
          className="flex items-center space-x-1 bg-void-light border border-slate-700 hover:border-cyan-neon text-slate-300 hover:text-cyan-neon text-xs px-3 py-1.5 rounded-xl transition font-mono"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Node</span>
        </button>
        <button
          onClick={onResetLayout}
          className="p-1.5 rounded-xl bg-void-light border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-slate-200 transition"
          title="Reset Canvas Layout"
        >
          <RefreshCw className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={onExport}
          className="flex items-center space-x-1 bg-void-light border border-slate-700 hover:border-purple-electric text-slate-300 hover:text-purple-electric text-xs px-3 py-1.5 rounded-xl transition font-mono"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export JSON</span>
        </button>
      </div>
    </div>
  );
}

