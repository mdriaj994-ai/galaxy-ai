import React, { useState } from 'react';
import { 
  Play, 
  CheckCircle2, 
  Clock, 
  MessageSquare, 
  Zap, 
  SendHorizontal,
  ChevronRight,
  Sparkles
} from 'lucide-react';

export default function AgentCard({ agent, onAssignTask, onStatusChange }) {
  const [showModal, setShowModal] = useState(false);
  const [taskInput, setTaskInput] = useState('');
  const [priority, setPriority] = useState('High');

  const statusColors = {
    Working: 'border-cyan-neon bg-cyan-neon/10 text-cyan-neon shadow-neon-cyan',
    Collaborating: 'border-purple-electric bg-purple-electric/10 text-purple-electric shadow-neon-purple',
    Idle: 'border-slate-700 bg-slate-800/40 text-slate-400',
  };

  const handleTaskSubmit = (e) => {
    e.preventDefault();
    if (!taskInput.trim()) return;
    onAssignTask(agent.name, taskInput.trim(), priority);
    setTaskInput('');
    setShowModal(false);
  };

  return (
    <div className="relative group bg-void-card border border-slate-800/80 hover:border-cyan-neon/50 rounded-2xl p-5 transition-all duration-300 hover:shadow-2xl flex flex-col justify-between overflow-hidden">
      {/* Background Cyber Accent */}
      <div 
        className="absolute -right-8 -top-8 w-32 h-32 rounded-full blur-3xl pointer-events-none opacity-20"
        style={{ background: agent.accentColor }}
      />

      {/* Header Info */}
      <div>
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div 
              className="w-12 h-12 rounded-xl flex items-center justify-center font-bold text-xl border shadow-lg"
              style={{ backgroundColor: `${agent.accentColor}20`, borderColor: agent.accentColor, color: agent.accentColor }}
            >
              {agent.avatarLetter}
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-100 flex items-center">
                {agent.name}
                <span className="ml-2 text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">
                  {agent.role}
                </span>
              </h3>
              <p className="text-xs text-slate-400 font-mono mt-0.5">{agent.specialty}</p>
            </div>
          </div>

          {/* Status Dropdown / Cycle Toggle */}
          <button
            onClick={() => {
              const statuses = ['Idle', 'Working', 'Collaborating'];
              const nextIndex = (statuses.indexOf(agent.status) + 1) % statuses.length;
              onStatusChange(agent.name, statuses[nextIndex]);
            }}
            className={`text-xs font-mono font-semibold px-2.5 py-1 rounded-full border transition-all ${statusColors[agent.status] || statusColors.Idle}`}
            title="Click to toggle status"
          >
            ● {agent.status}
          </button>
        </div>

        {/* Current Focus Activity */}
        <div className="bg-void-light/70 rounded-xl p-3 border border-slate-800/80 mb-4">
          <span className="text-[10px] font-mono text-slate-500 uppercase flex items-center">
            <Zap className="w-3 h-3 text-cyan-neon mr-1" /> Active Focus
          </span>
          <p className="text-xs text-slate-200 mt-1 font-medium leading-relaxed">
            "{agent.currentFocus}"
          </p>
        </div>

        {/* Live Tasks List */}
        <div className="space-y-1.5 mb-4">
          <div className="text-[10px] font-mono text-slate-500 uppercase flex justify-between items-center">
            <span>Recent Task Queue</span>
            <span>{agent.tasks?.length || 0} items</span>
          </div>
          {agent.tasks && agent.tasks.length > 0 ? (
            agent.tasks.slice(0, 2).map((t, idx) => (
              <div 
                key={idx} 
                className="flex items-center justify-between text-xs bg-slate-900/60 px-2.5 py-1.5 rounded-lg border border-slate-800/50"
              >
                <span className="truncate max-w-[200px] text-slate-300">{t.title}</span>
                <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${
                  t.priority === 'Urgent' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                  t.priority === 'High' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                  'bg-cyan-neon/10 text-cyan-neon'
                }`}>
                  {t.priority}
                </span>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-500 italic">No pending tasks in queue.</p>
          )}
        </div>
      </div>

      {/* Action Footer */}
      <div className="pt-3 border-t border-slate-800/60 flex items-center justify-between">
        <span className="text-[11px] font-mono text-slate-400 flex items-center">
          <Clock className="w-3 h-3 mr-1 text-slate-500" /> Latency: 12ms
        </span>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center space-x-1.5 bg-gradient-to-r from-cyan-neon to-purple-electric hover:opacity-90 text-void font-bold text-xs px-3.5 py-1.5 rounded-lg transition shadow-neon-cyan"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Hand Over Task</span>
        </button>
      </div>

      {/* Face-to-Face Task Handover Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-void/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-void-card border border-cyan-neon/40 rounded-2xl p-6 max-w-md w-full shadow-2xl relative animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <div 
                  className="w-7 h-7 rounded-lg flex items-center justify-center font-bold text-sm"
                  style={{ backgroundColor: `${agent.accentColor}25`, color: agent.accentColor }}
                >
                  {agent.avatarLetter}
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-100">Hand Over Task to {agent.name}</h4>
                  <p className="text-[10px] text-slate-400 font-mono">Direct Face-to-Face Assignment</p>
                </div>
              </div>
              <button 
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-slate-100 p-1"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleTaskSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5">Task Objective or Brief</label>
                <textarea
                  value={taskInput}
                  onChange={(e) => setTaskInput(e.target.value)}
                  placeholder={`Describe what you want ${agent.name} to accomplish...`}
                  rows={4}
                  className="w-full bg-void-light border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-neon font-sans"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1.5">Execution Priority</label>
                <div className="grid grid-cols-3 gap-2">
                  {['Low', 'Medium', 'High', 'Urgent'].slice(1).map((p) => (
                    <button
                      type="button"
                      key={p}
                      onClick={() => setPriority(p)}
                      className={`py-1.5 rounded-lg text-xs font-mono font-semibold border transition ${
                        priority === p 
                          ? 'border-cyan-neon bg-cyan-neon/20 text-cyan-neon shadow-neon-cyan' 
                          : 'border-slate-800 bg-void-light text-slate-400 hover:border-slate-700'
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-3.5 py-1.5 rounded-lg text-xs font-mono text-slate-400 hover:text-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex items-center space-x-1.5 bg-cyan-neon hover:bg-cyan-neon/90 text-void font-bold text-xs px-4 py-2 rounded-xl transition shadow-neon-cyan"
                >
                  <SendHorizontal className="w-3.5 h-3.5" />
                  <span>Assign Instantly</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

