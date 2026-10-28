import React, { useState, useEffect } from 'react';
import { Database, Plus, Trash2, Search, Tag, Calendar, RefreshCw } from 'lucide-react';

export default function MemoryManager() {
  const [memories, setMemories] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');
  const [newCategory, setNewCategory] = useState('Personal');
  const [showAddForm, setShowAddForm] = useState(false);

  const loadMemories = async () => {
    if (window.galaxyBridge?.getMemories) {
      try {
        const data = await window.galaxyBridge.getMemories();
        setMemories(data || []);
      } catch (e) {
        console.warn('Memory load error:', e);
      }
    }
  };

  useEffect(() => {
    loadMemories();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newKey.trim() || !newValue.trim()) return;

    if (window.galaxyBridge?.saveMemory) {
      await window.galaxyBridge.saveMemory(newKey.trim(), newValue.trim(), newCategory);
      await window.galaxyBridge.logEvent('MEMORY_CREATED', `Saved memory [${newKey}]`);
    }

    setNewKey('');
    setNewValue('');
    setShowAddForm(false);
    loadMemories();
  };

  const handleDelete = async (id) => {
    if (window.galaxyBridge?.deleteMemory) {
      await window.galaxyBridge.deleteMemory(id);
      await window.galaxyBridge.logEvent('MEMORY_DELETED', `Deleted memory ID ${id}`);
    }
    loadMemories();
  };

  const filteredMemories = memories.filter(
    (m) =>
      m.key?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.value?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.category?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-void-card border border-slate-800/80 rounded-2xl p-6 flex flex-col space-y-5">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center">
            <Database className="w-4 h-4 text-cyan-neon mr-2" />
            LOCAL SQLITE MEMORY INSPECTOR
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Zero-cloud persistent user context and preferences stored locally.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={loadMemories}
            className="p-1.5 rounded-lg bg-void-light border border-slate-800 text-slate-400 hover:text-slate-100 transition"
            title="Refresh memory table"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center space-x-1.5 bg-cyan-neon hover:bg-cyan-neon/90 text-void font-bold text-xs px-3.5 py-1.5 rounded-lg transition shadow-neon-cyan"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Memory</span>
          </button>
        </div>
      </div>

      {/* Search Input */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search key, value, or category in local SQLite tables..."
          className="w-full bg-void-light border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-neon font-mono"
        />
      </div>

      {/* Add Memory Modal/Inline Form */}
      {showAddForm && (
        <form onSubmit={handleAdd} className="bg-void-light/80 p-4 rounded-xl border border-cyan-neon/30 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
            <input
              type="text"
              value={newKey}
              onChange={(e) => setNewKey(e.target.value)}
              placeholder="Memory Key (e.g. Favorite Editor)"
              className="bg-void border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-100 font-mono focus:border-cyan-neon"
            />
            <input
              type="text"
              value={newValue}
              onChange={(e) => setNewValue(e.target.value)}
              placeholder="Value (e.g. VS Code with Cyberpunk Theme)"
              className="bg-void border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-100 font-mono focus:border-cyan-neon"
            />
            <select
              value={newCategory}
              onChange={(e) => setNewCategory(e.target.value)}
              className="bg-void border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-300 font-mono focus:border-cyan-neon"
            >
              <option value="Personal">Personal Preference</option>
              <option value="System">System & Hardware</option>
              <option value="Work">Workspace & Project</option>
              <option value="AI">AI Prompt Style</option>
            </select>
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={() => setShowAddForm(false)}
              className="px-3 py-1 rounded-lg text-xs font-mono text-slate-400 hover:text-slate-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-3.5 py-1 rounded-lg text-xs font-mono font-bold bg-cyan-neon text-void"
            >
              Commit to SQLite
            </button>
          </div>
        </form>
      )}

      {/* Memories Table / Grid */}
      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
        {filteredMemories.length > 0 ? (
          filteredMemories.map((m) => (
            <div
              key={m.id || m.key}
              className="bg-void-light/50 border border-slate-800/80 hover:border-slate-700 rounded-xl p-3 flex items-center justify-between transition"
            >
              <div className="flex-1 pr-4">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="text-xs font-bold font-mono text-slate-100">{m.key}</span>
                  <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-cyan-neon border border-slate-700 flex items-center">
                    <Tag className="w-2.5 h-2.5 mr-1" />
                    {m.category || 'General'}
                  </span>
                </div>
                <p className="text-xs text-slate-300 font-sans">{m.value}</p>
              </div>

              <div className="flex items-center space-x-3">
                <span className="hidden sm:flex items-center text-[10px] text-slate-500 font-mono">
                  <Calendar className="w-3 h-3 mr-1" />
                  {m.created_at ? new Date(m.created_at).toLocaleDateString() : 'Active'}
                </span>
                <button
                  onClick={() => handleDelete(m.id)}
                  className="p-1.5 rounded text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition"
                  title="Delete from SQLite"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="p-8 text-center text-slate-500 font-mono text-xs">
            No memory entries found. Click "+ Add Memory" to write directly to SQLite.
          </div>
        )}
      </div>
    </div>
  );
}

