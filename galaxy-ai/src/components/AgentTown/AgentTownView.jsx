import React, { useState, useEffect } from 'react';
import AgentCard from './AgentCard';
import { Users, Sparkles, RefreshCw, Terminal, Layers } from 'lucide-react';

export default function AgentTownView() {
  const [agents, setAgents] = useState([
    {
      name: 'Alice',
      role: 'Chief Researcher',
      specialty: 'Web scraping, literature review & local document indexing',
      avatarLetter: 'A',
      accentColor: '#00F0FF',
      status: 'Working',
      currentFocus: 'Extracting key data points from local engineering repositories',
      tasks: [
        { title: 'Index SQLite performance benchmarks', priority: 'High', status: 'Working' },
        { title: 'Catalog zero-cloud offline LLM runtime papers', priority: 'Medium', status: 'Pending' },
      ],
    },
    {
      name: 'Bob',
      role: 'Full-Stack Developer',
      specialty: 'Electron IPC, React components & OS automations',
      avatarLetter: 'B',
      accentColor: '#7000FF',
      status: 'Collaborating',
      currentFocus: 'Writing system automation scripts for WhatsApp & File Manager sync',
      tasks: [
        { title: 'Optimize IPC bridge message serialization', priority: 'Urgent', status: 'Working' },
      ],
    },
    {
      name: 'Carol',
      role: 'Creative Director',
      specialty: 'Cyberpunk UI design, canvas diagrams & voice tones',
      avatarLetter: 'C',
      accentColor: '#EC4899',
      status: 'Working',
      currentFocus: 'Tuning futuristic neon color balances & holographic orb glow',
      tasks: [
        { title: 'Create interactive MindMap layout nodes', priority: 'High', status: 'Working' },
      ],
    },
    {
      name: 'Dave',
      role: 'Data Analyst',
      specialty: 'Local database metrics, memory categorization & system logs',
      avatarLetter: 'D',
      accentColor: '#10B981',
      status: 'Idle',
      currentFocus: 'Awaiting next real-time database indexing instructions',
      tasks: [],
    },
  ]);

  const [officeLog, setOfficeLog] = useState([]);

  useEffect(() => {
    // Load persisted tasks from local SQLite
    const loadPersistedTasks = async () => {
      if (window.galaxyBridge?.getAgentTasks) {
        try {
          const allTasks = await window.galaxyBridge.getAgentTasks();
          if (allTasks && allTasks.length > 0) {
            setAgents((prev) =>
              prev.map((agent) => {
                const agentTasks = allTasks.filter((t) => t.agent.toLowerCase() === agent.name.toLowerCase());
                return {
                  ...agent,
                  tasks: agentTasks.length > 0 ? agentTasks : agent.tasks,
                };
              })
            );
          }
        } catch (e) {
          console.warn('Task load error:', e);
        }
      }
    };

    loadPersistedTasks();

    setOfficeLog([
      '[Alice] Extracted 42 local references into SQLite memory.',
      '[Bob] Connected WhatsApp automated media delivery handler.',
      '[Carol] Canvas diagrams responsive engine calibrated.',
      '[Dave] System memory usage verified within normal threshold.',
    ]);
  }, []);

  const handleAssignTask = async (agentName, taskTitle, priority) => {
    // Save to SQLite
    if (window.galaxyBridge?.addAgentTask) {
      await window.galaxyBridge.addAgentTask(agentName, taskTitle, priority, 'Working');
      await window.galaxyBridge.logEvent('TASK_ASSIGNED', `${agentName} was assigned: ${taskTitle}`);
    }

    setAgents((prev) =>
      prev.map((agent) => {
        if (agent.name === agentName) {
          return {
            ...agent,
            status: 'Working',
            currentFocus: taskTitle,
            tasks: [{ title: taskTitle, priority, status: 'Working' }, ...agent.tasks],
          };
        }
        return agent;
      })
    );

    setOfficeLog((prev) => [`[${agentName}] Received new task: "${taskTitle}" (${priority})`, ...prev.slice(0, 5)]);
  };

  const handleStatusChange = async (agentName, newStatus) => {
    setAgents((prev) =>
      prev.map((agent) => (agent.name === agentName ? { ...agent, status: newStatus } : agent))
    );

    if (window.galaxyBridge?.logEvent) {
      await window.galaxyBridge.logEvent('AGENT_STATUS_CHANGE', `${agentName} status changed to ${newStatus}`);
    }
  };

  return (
    <div className="h-full flex flex-col p-6 space-y-6 overflow-y-auto">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800/80 gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-cyan-neon" />
            <h2 className="text-xl font-bold tracking-wide text-slate-100">
              AGENT TOWN <span className="text-xs font-mono text-cyan-neon font-normal">/ VIRTUAL DESK ENGINE</span>
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">
            4 Autonomous Virtual Specialists collaborating inside your local operating environment.
          </p>
        </div>

        {/* Office Status Summary */}
        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="bg-void-card border border-slate-800 px-3 py-1.5 rounded-xl flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-cyan-neon animate-pulse" />
            <span className="text-slate-300">Working: {agents.filter((a) => a.status === 'Working').length}</span>
          </div>
          <div className="bg-void-card border border-slate-800 px-3 py-1.5 rounded-xl flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-purple-electric animate-pulse" />
            <span className="text-slate-300">Collaborating: {agents.filter((a) => a.status === 'Collaborating').length}</span>
          </div>
          <div className="bg-void-card border border-slate-800 px-3 py-1.5 rounded-xl flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-slate-500" />
            <span className="text-slate-400">Idle: {agents.filter((a) => a.status === 'Idle').length}</span>
          </div>
        </div>
      </div>

      {/* 4-Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        {agents.map((agent) => (
          <AgentCard
            key={agent.name}
            agent={agent}
            onAssignTask={handleAssignTask}
            onStatusChange={handleStatusChange}
          />
        ))}
      </div>

      {/* Live Collaboration Console Log */}
      <div className="bg-void-card border border-slate-800/80 rounded-2xl p-4 flex flex-col space-y-2">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 border-b border-slate-800 pb-2">
          <span className="flex items-center space-x-1.5 text-cyan-neon font-semibold">
            <Terminal className="w-4 h-4" />
            <span>REAL-TIME AGENT TELEMETRY LOG</span>
          </span>
          <span className="text-[10px] text-slate-500">Local-First Pipeline</span>
        </div>
        <div className="space-y-1 font-mono text-xs">
          {officeLog.map((log, i) => (
            <p key={i} className="text-slate-300 leading-relaxed flex items-center space-x-2">
              <span className="text-slate-600">›</span>
              <span>{log}</span>
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}

