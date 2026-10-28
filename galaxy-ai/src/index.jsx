import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/globals.css';

// Browser fallback mockup if opened outside Electron
if (!window.galaxyBridge) {
  console.info('[Galaxy AI] Running in browser mode — using virtual bridge.');
  const virtualStorage = {
    memories: [
      { id: 1, key: 'User Nickname', value: 'Commander', category: 'Profile', created_at: new Date().toISOString() },
      { id: 2, key: 'Preferred Model', value: 'Local-First Deep Neural Core', category: 'AI', created_at: new Date().toISOString() },
      { id: 3, key: 'Primary Workplace', value: 'D:\\Galaxy Projects', category: 'System', created_at: new Date().toISOString() },
    ],
    tasks: [
      { id: 101, agent: 'Alice', title: 'Deep dive into Local-first LLM Quantization', priority: 'High', status: 'Working' },
      { id: 102, agent: 'Bob', title: 'Compile SQLite WAL mode optimizations', priority: 'Urgent', status: 'Working' },
      { id: 103, agent: 'Carol', title: 'Design futuristic Holo-HUD interface', priority: 'Medium', status: 'Collaborating' },
      { id: 104, agent: 'Dave', title: 'Analyze system memory telemetry trends', priority: 'Low', status: 'Idle' },
    ],
    settings: {
      theme: 'cyberpunk',
      soul_tone: 'jarvis',
      user_name: 'Commander',
      license_active: 'true',
    },
    logs: [
      { id: 1, event_type: 'SYSTEM_BOOT', details: 'Galaxy AI Core v1.0 initialized successfully.', timestamp: new Date().toLocaleTimeString() },
      { id: 2, event_type: 'MEMORY_SYNC', details: 'Local SQLite engine loaded with zero cloud dependencies.', timestamp: new Date().toLocaleTimeString() },
    ],
  };

  window.galaxyBridge = {
    getMemories: async () => virtualStorage.memories,
    saveMemory: async ({ key, value, category }) => {
      virtualStorage.memories.unshift({ id: Date.now(), key, value, category, created_at: new Date().toISOString() });
      return true;
    },
    deleteMemory: async (id) => {
      virtualStorage.memories = virtualStorage.memories.filter((m) => m.id !== id);
      return true;
    },
    getAgentTasks: async (agentName) => {
      if (agentName) return virtualStorage.tasks.filter((t) => t.agent.toLowerCase() === agentName.toLowerCase());
      return virtualStorage.tasks;
    },
    addAgentTask: async ({ agent, title, priority, status }) => {
      const t = { id: Date.now(), agent, title, priority, status: status || 'Working' };
      virtualStorage.tasks.unshift(t);
      return t;
    },
    updateTaskStatus: async ({ id, status }) => {
      const item = virtualStorage.tasks.find((t) => t.id === id);
      if (item) item.status = status;
      return true;
    },
    getLogs: async () => virtualStorage.logs,
    logEvent: async ({ eventType, details }) => {
      virtualStorage.logs.unshift({ id: Date.now(), event_type: eventType, details, timestamp: new Date().toLocaleTimeString() });
    },
    getSettings: async () => virtualStorage.settings,
    saveSetting: async ({ key, value }) => {
      virtualStorage.settings[key] = value;
      return true;
    },
    launchApp: async (app) => ({ success: true, message: `Simulated launching ${app}` }),
    openFolder: async (f) => ({ success: true, path: f }),
    listDirectory: async () => ({ success: true, files: [] }),
    getSystemMetrics: async () => ({
      platform: 'win32 (Simulated)',
      hostname: 'GALAXY-STATION-01',
      uptimeHours: 14,
      cpuModel: 'Intel Core i9 / AMD Ryzen Hyper-Thread',
      cpuCount: 16,
      memoryTotalGB: '32.00',
      memoryUsedGB: '11.84',
      memoryUsagePercent: 37,
    }),
    fetchUrl: async (url) => ({ success: true, url, title: 'Simulated Page', snippet: 'Preview content fetched locally.' }),
    getGlobalFeeds: async () => [
      { id: 1, source: 'GALAXY EDGE RADAR', headline: 'Local SQLite Engine synchronizing at 1,200 ops/sec', urgency: 'INFO', region: 'Global Node', timestamp: 'Just now' },
      { id: 2, source: 'SECURE AGENT MESH', headline: 'Alice and Bob successfully handed off Code Review task', urgency: 'HIGH', region: 'Sector 4', timestamp: '2m ago' },
      { id: 3, source: 'MOBILE TELEMETRY', headline: 'Android companion device connected via Local WebSocket', urgency: 'NORMAL', region: 'Handheld', timestamp: '5m ago' },
    ],
    minimizeWindow: () => {},
    maximizeWindow: () => {},
    closeWindow: () => {},
  };
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

