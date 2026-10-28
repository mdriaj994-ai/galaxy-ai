import React, { useState } from 'react';
import VoiceChatPanel from './VoiceChatPanel';
import { Smartphone, Wifi, Battery, Signal, ArrowLeft, MoreVertical, Mic, Volume2 } from 'lucide-react';

export default function MobileSimulator() {
  const [activeIntentPopup, setActiveIntentPopup] = useState(null);

  const handleTriggerIntent = (intentName) => {
    setActiveIntentPopup(`Dispatched Android Intent: ${intentName}`);
    setTimeout(() => setActiveIntentPopup(null), 3000);
  };

  return (
    <div className="h-full flex flex-col p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
        <div>
          <div className="flex items-center space-x-2">
            <Smartphone className="w-5 h-5 text-cyan-neon" />
            <h2 className="text-xl font-bold tracking-wide text-slate-100">
              ANDROID SYNC <span className="text-xs font-mono text-cyan-neon font-normal">/ COMPANION SIMULATOR</span>
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Simulate and interact with your cross-platform React Native Android companion codebase in real-time.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-slate-300">Android Link: Active (WebSocket Peer)</span>
        </div>
      </div>

      {/* Main Container: Android Phone Mockup + Control Telemetry */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start flex-1">
        {/* Android Phone Frame */}
        <div className="lg:col-span-5 flex justify-center">
          <div className="relative w-[340px] h-[640px] bg-black rounded-[44px] p-3 shadow-2xl border-[4px] border-slate-700/80 ring-1 ring-cyan-neon/30 flex flex-col overflow-hidden">
            {/* Phone Speaker Notch & Camera Pin */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-5 bg-black rounded-b-xl z-30 flex items-center justify-center space-x-3">
              <div className="w-10 h-1 bg-slate-800 rounded-full" />
              <div className="w-2.5 h-2.5 bg-slate-900 border border-slate-700 rounded-full" />
            </div>

            {/* Android Screen Display */}
            <div className="flex-1 bg-void rounded-[34px] overflow-hidden flex flex-col pt-5 relative">
              {/* Status Bar */}
              <div className="flex items-center justify-between px-5 py-1 text-[11px] font-mono text-slate-400 border-b border-slate-900 select-none">
                <span>12:00</span>
                <div className="flex items-center space-x-2">
                  <Signal className="w-3 h-3" />
                  <Wifi className="w-3 h-3 text-cyan-neon" />
                  <Battery className="w-3.5 h-3.5 text-emerald-400" />
                </div>
              </div>

              {/* App Bar */}
              <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-void-light/50">
                <div className="flex items-center space-x-2">
                  <div className="w-6 h-6 rounded-lg bg-gradient-to-tr from-purple-electric to-cyan-neon flex items-center justify-center font-bold text-xs text-void">
                    G
                  </div>
                  <span className="text-xs font-bold text-slate-200">Galaxy Mobile</span>
                </div>
                <MoreVertical className="w-4 h-4 text-slate-400" />
              </div>

              {/* In-Phone Screen Content */}
              <div className="flex-1 p-2 flex flex-col overflow-hidden">
                <VoiceChatPanel onTriggerIntent={handleTriggerIntent} />
              </div>

              {/* Android Toast/Intent Notification Bar */}
              {activeIntentPopup && (
                <div className="absolute top-16 left-4 right-4 bg-purple-electric text-white p-2.5 rounded-xl text-xs font-mono shadow-2xl animate-in fade-in slide-in-from-top duration-200 z-50 flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-white animate-ping" />
                  <span>{activeIntentPopup}</span>
                </div>
              )}

              {/* Bottom Android Gesture Navigation Bar */}
              <div className="h-4 flex items-center justify-center pb-1">
                <div className="w-24 h-1 bg-slate-700 rounded-full" />
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Companion Code & Service Inspector */}
        <div className="lg:col-span-7 flex flex-col space-y-4">
          <div className="bg-void-card border border-slate-800/80 rounded-2xl p-5">
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider mb-2">
              React Native Android Architecture
            </h3>
            <p className="text-xs text-slate-400 font-sans leading-relaxed mb-4">
              The companion application located in <code className="text-cyan-neon font-mono bg-void-light px-1.5 py-0.5 rounded">/mobile</code> runs natively on Android with intent services, vocal capture, and document parsing capabilities.
            </p>

            <div className="space-y-2 font-mono text-xs">
              <div className="p-3 rounded-xl bg-void-light border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-cyan-neon font-bold block">VoiceScreen.js</span>
                  <span className="text-slate-400 text-[11px]">Android voice intent launcher with offline wake word</span>
                </div>
                <span className="text-[10px] text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/20">READY</span>
              </div>

              <div className="p-3 rounded-xl bg-void-light border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-purple-electric font-bold block">ChatScreen.js</span>
                  <span className="text-slate-400 text-[11px]">PDF & Image multi-modal document extractor</span>
                </div>
                <span className="text-[10px] text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/20">READY</span>
              </div>

              <div className="p-3 rounded-xl bg-void-light border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-pink-400 font-bold block">DeviceControl.js</span>
                  <span className="text-slate-400 text-[11px]">Native Android intents: YouTube, Facebook, Alarms, Volume</span>
                </div>
                <span className="text-[10px] text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/20">ACTIVE</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

