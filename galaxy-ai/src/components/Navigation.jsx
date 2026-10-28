import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Mic2, 
  Globe, 
  Network, 
  Smartphone, 
  Cpu, 
  ShieldCheck, 
  Minus, 
  Square, 
  X,
  Activity,
  Terminal
} from 'lucide-react';

export default function Navigation({ activeTab, setActiveTab }) {
  const [metrics, setMetrics] = useState({ memoryUsagePercent: 35, cpuCount: 8 });
  const [currentTime, setCurrentTime] = useState(new Date().toUTCString().slice(17, 25) + ' UTC');

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toUTCString().slice(17, 25) + ' UTC');
    }, 1000);

    const fetchMetrics = async () => {
      if (window.galaxyBridge?.getSystemMetrics) {
        try {
          const data = await window.galaxyBridge.getSystemMetrics();
          setMetrics(data);
        } catch (e) {
          console.warn('Metrics fetch error:', e);
        }
      }
    };

    fetchMetrics();
    const metricTimer = setInterval(fetchMetrics, 5000);

    return () => {
      clearInterval(timer);
      clearInterval(metricTimer);
    };
  }, []);

  const navItems = [
    { id: 'agent-town', label: 'Agent Town', icon: Users, badge: '4 Active' },
    { id: 'voice-soul', label: 'Voice & Soul', icon: Mic2, badge: 'Live Core' },
    { id: 'world-monitor', label: 'World Monitor', icon: Globe, badge: 'Global 3D' },
    { id: 'diagram-gen', label: 'Diagram Engine', icon: Network, badge: 'AI Mindmap' },
    { id: 'android-sync', label: 'Android Sync', icon: Smartphone, badge: 'Companion' },
  ];

  return (
    <header className="h-16 border-b border-void-light bg-void/90 backdrop-blur-md flex items-center justify-between px-4 z-50 select-none">
      {/* Brand & System Status */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-electric to-cyan-neon flex items-center justify-center shadow-neon-cyan">
            <span className="font-bold text-void text-lg tracking-wider">G</span>
          </div>
          <div>
            <h1 className="font-bold tracking-wider text-slate-100 flex items-center text-sm">
              GALAXY AI <span className="ml-2 text-[10px] text-cyan-neon font-mono px-1.5 py-0.5 rounded bg-cyan-neon/10 border border-cyan-neon/30">CORE v1.0</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-mono tracking-tight flex items-center">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping mr-1"></span>
              LOCAL-FIRST RUNTIME (SQLITE)
            </p>
          </div>
        </div>

        {/* System HUD Badges */}
        <div className="hidden lg:flex items-center space-x-3 text-xs font-mono border-l border-slate-800 pl-4">
          <div className="flex items-center space-x-1.5 text-slate-300 bg-void-light px-2.5 py-1 rounded border border-slate-800">
            <Cpu className="w-3.5 h-3.5 text-cyan-neon" />
            <span>RAM {metrics.memoryUsagePercent}%</span>
          </div>
          <div className="flex items-center space-x-1.5 text-slate-300 bg-void-light px-2.5 py-1 rounded border border-slate-800">
            <Activity className="w-3.5 h-3.5 text-purple-electric" />
            <span>{currentTime}</span>
          </div>
          <div className="flex items-center space-x-1.5 text-emerald-400 bg-emerald-950/30 px-2.5 py-1 rounded border border-emerald-500/20">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>LICENSE VERIFIED</span>
          </div>
        </div>
      </div>

      {/* Main Module Tabs */}
      <nav className="flex items-center space-x-1 bg-void-light p-1 rounded-xl border border-slate-800">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200 ${
                isActive
                  ? 'bg-gradient-to-r from-cyan-neon/20 to-purple-electric/20 text-cyan-neon border border-cyan-neon/40 shadow-neon-cyan'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-neon animate-pulse' : 'text-slate-400'}`} />
              <span>{item.label}</span>
              {isActive && (
                <span className="hidden xl:inline text-[9px] font-mono bg-cyan-neon/20 text-cyan-neon px-1.5 py-0.2 rounded-full">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Window Controls (Electron Native Look) */}
      <div className="flex items-center space-x-2">
        <button
          onClick={() => window.galaxyBridge?.minimizeWindow?.()}
          className="w-7 h-7 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-100 flex items-center justify-center transition"
          title="Minimize"
        >
          <Minus className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => window.galaxyBridge?.maximizeWindow?.()}
          className="w-7 h-7 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-100 flex items-center justify-center transition"
          title="Maximize"
        >
          <Square className="w-3 h-3" />
        </button>
        <button
          onClick={() => window.galaxyBridge?.closeWindow?.()}
          className="w-7 h-7 rounded hover:bg-red-500/20 text-slate-400 hover:text-red-400 flex items-center justify-center transition"
          title="Close"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </header>
  );
}

