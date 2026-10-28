import React, { useState } from 'react';
import Navigation from './components/Navigation';
import AgentTownView from './components/AgentTown/AgentTownView';
import VoiceAssistant from './components/VoiceSoul/VoiceAssistant';
import CommandMap from './components/WorldMonitor/CommandMap';
import DiagramCanvas from './components/DiagramGen/DiagramCanvas';
import MobileSimulator from './components/AndroidSync/MobileSimulator';

export default function App() {
  const [activeTab, setActiveTab] = useState('voice-soul');

  return (
    <div className="h-screen w-screen flex flex-col bg-void text-slate-100 overflow-hidden select-none font-sans">
      {/* Top Header & HUD Navigation */}
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main View Port */}
      <main className="flex-1 overflow-hidden relative">
        {activeTab === 'agent-town' && <AgentTownView />}
        {activeTab === 'voice-soul' && <VoiceAssistant />}
        {activeTab === 'world-monitor' && <CommandMap />}
        {activeTab === 'diagram-gen' && <DiagramCanvas />}
        {activeTab === 'android-sync' && <MobileSimulator />}
      </main>
    </div>
  );
}

