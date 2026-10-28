import React, { useState, useEffect } from 'react';
import Globe3D from './Globe3D';
import NewsFeed from './NewsFeed';
import { Globe, Clock, ShieldAlert, Cpu, Activity, Compass } from 'lucide-react';

export default function CommandMap() {
  const [clocks, setClocks] = useState({
    utc: '',
    tokyo: '',
    london: '',
    newyork: '',
    dhaka: '',
  });

  useEffect(() => {
    const updateClocks = () => {
      const now = new Date();
      setClocks({
        utc: now.toLocaleTimeString('en-US', { timeZone: 'UTC', hour12: false }),
        london: now.toLocaleTimeString('en-US', { timeZone: 'Europe/London', hour12: false }),
        newyork: now.toLocaleTimeString('en-US', { timeZone: 'America/New_York', hour12: false }),
        tokyo: now.toLocaleTimeString('en-US', { timeZone: 'Asia/Tokyo', hour12: false }),
        dhaka: now.toLocaleTimeString('en-US', { timeZone: 'Asia/Dhaka', hour12: false }),
      });
    };

    updateClocks();
    const interval = setInterval(updateClocks, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full flex flex-col p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800/80 gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <Globe className="w-5 h-5 text-cyan-neon" />
            <h2 className="text-xl font-bold tracking-wide text-slate-100">
              WORLD MONITOR <span className="text-xs font-mono text-cyan-neon font-normal">/ GLOBAL COMMAND RADAR</span>
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Real-time orbital tracking, global multi-timezone telemetry, and autonomous cyber news parser.
          </p>
        </div>

        {/* Global Clocks Bar */}
        <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
          {[
            { city: 'UTC (Zulu)', time: clocks.utc, color: 'text-cyan-neon' },
            { city: 'New York', time: clocks.newyork, color: 'text-slate-300' },
            { city: 'London', time: clocks.london, color: 'text-slate-300' },
            { city: 'Dhaka', time: clocks.dhaka, color: 'text-emerald-400' },
            { city: 'Tokyo', time: clocks.tokyo, color: 'text-purple-electric' },
          ].map((c) => (
            <div key={c.city} className="bg-void-card border border-slate-800 px-3 py-1.5 rounded-xl">
              <span className="text-[10px] text-slate-500 block">{c.city}</span>
              <span className={`font-bold ${c.color}`}>{c.time || '--:--:--'}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Main Grid: 3D Globe + News Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: 3D Globe & Hotspots */}
        <div className="lg:col-span-7 flex flex-col space-y-4">
          <Globe3D />

          {/* Hotspots Summary Card */}
          <div className="bg-void-card border border-slate-800/80 rounded-2xl p-4">
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block mb-3">
              ACTIVE INTELLIGENCE TELEMETRY NODES
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs font-mono">
              {[
                { name: 'Silicon Valley', ping: '18ms', status: 'Optimal', color: 'text-cyan-neon' },
                { name: 'London Node', ping: '42ms', status: 'Nominal', color: 'text-purple-electric' },
                { name: 'Tokyo Relay', ping: '65ms', status: 'Optimal', color: 'text-pink-400' },
                { name: 'Dhaka Command', ping: '8ms', status: 'Local Host', color: 'text-emerald-400' },
                { name: 'Frankfurt Hub', ping: '54ms', status: 'Nominal', color: 'text-slate-300' },
                { name: 'Singapore Link', ping: '38ms', status: 'Optimal', color: 'text-cyan-neon' },
              ].map((node) => (
                <div key={node.name} className="p-2.5 rounded-xl bg-void-light/60 border border-slate-800">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-slate-200">{node.name}</span>
                    <span className="text-[9px] text-slate-500">{node.ping}</span>
                  </div>
                  <span className={`text-[10px] ${node.color} flex items-center`}>
                    <span className="w-1.5 h-1.5 rounded-full bg-current mr-1" />
                    {node.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: News & RSS Feed Parser */}
        <div className="lg:col-span-5 flex flex-col">
          <NewsFeed />
        </div>
      </div>
    </div>
  );
}

