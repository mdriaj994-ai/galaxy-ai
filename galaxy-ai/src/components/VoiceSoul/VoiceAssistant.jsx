import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, Sparkles, Terminal, ArrowUpRight, Zap } from 'lucide-react';
import SoulTuner from './SoulTuner';
import MemoryManager from './MemoryManager';

export default function VoiceAssistant() {
  const [isListening, setIsListening] = useState(false);
  const [aiState, setAiState] = useState('idle'); // 'idle', 'listening', 'thinking', 'speaking'
  const [transcript, setTranscript] = useState('');
  const [aiResponse, setAiResponse] = useState('Online and calibrated. Awaiting your voice or text directives, Commander.');
  const [activeSubTab, setActiveSubTab] = useState('orb'); // 'orb', 'soul', 'memory'

  const canvasRef = useRef(null);

  // Audio waveform animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let phase = 0;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;
      const centerY = height / 2;

      ctx.beginPath();
      ctx.lineWidth = 2;

      // Color based on AI state
      if (aiState === 'listening') {
        ctx.strokeStyle = '#00F0FF';
      } else if (aiState === 'thinking') {
        ctx.strokeStyle = '#7000FF';
      } else if (aiState === 'speaking') {
        ctx.strokeStyle = '#EC4899';
      } else {
        ctx.strokeStyle = '#334155';
      }

      const amplitude = aiState === 'listening' ? 28 : aiState === 'speaking' ? 38 : aiState === 'thinking' ? 18 : 6;
      const frequency = 0.04;

      for (let x = 0; x < width; x++) {
        const y = centerY + Math.sin(x * frequency + phase) * amplitude * Math.sin((x / width) * Math.PI);
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.stroke();

      phase += 0.08;
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animationFrameId);
  }, [aiState]);

  // Voice recognition simulation / Web Speech API
  const toggleListening = () => {
    if (isListening) {
      setIsListening(false);
      setAiState('idle');
    } else {
      setIsListening(true);
      setAiState('listening');
      setTranscript('Listening for vocal frequency...');

      // Check if browser SpeechRecognition is available
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        try {
          const recognition = new SpeechRecognition();
          recognition.lang = 'en-US';
          recognition.onresult = (event) => {
            const spoken = event.results[0][0].transcript;
            setTranscript(spoken);
            processVoiceCommand(spoken);
          };
          recognition.onerror = () => {
            simulateCommand();
          };
          recognition.start();
        } catch (e) {
          simulateCommand();
        }
      } else {
        simulateCommand();
      }
    }
  };

  const simulateCommand = () => {
    setTimeout(() => {
      const sampleCommands = [
        'Open file manager and check D drive',
        'Launch calculator for quick equations',
        'Summarize quantum protocol telemetry',
        'Create high priority research task for Alice',
      ];
      const pick = sampleCommands[Math.floor(Math.random() * sampleCommands.length)];
      setTranscript(pick);
      processVoiceCommand(pick);
    }, 2000);
  };

  const processVoiceCommand = async (command) => {
    setAiState('thinking');
    setIsListening(false);

    let reply = `Executing directive: "${command}"...`;

    // Try calling the active Universal Agent Python Server
    try {
      const res = await fetch('http://127.0.0.1:5000/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
      });
      if (res.ok) {
        const data = await res.json();
        reply = data.reply || reply;
      }
    } catch (err) {
      // Fallback to Electron IPC Bridge if Python server is not reachable
      const low = command.toLowerCase();
      if (low.includes('calculator') || low.includes('calc')) {
        await window.galaxyBridge?.launchApp?.('calc');
        reply = 'ক্যালকুলেটর চালু হচ্ছে।';
      } else if (low.includes('photoshop')) {
        await window.galaxyBridge?.launchApp?.('photoshop');
        reply = 'ফটোশপ চালু হচ্ছে।';
      } else if (low.includes('notepad')) {
        await window.galaxyBridge?.launchApp?.('notepad');
        reply = 'নোটপ্যাড চালু হচ্ছে।';
      } else if (low.includes('d drive') || low.includes('file manager') || low.includes('explorer')) {
        await window.galaxyBridge?.openFolder?.('D:\\');
        reply = 'ডি ড্রাইভ ফাইল এক্সপ্লোরারে খোলা হয়েছে।';
      }
    }

    setAiState('speaking');
    setAiResponse(reply);

    // Local Speech Synthesis
    if (window.speechSynthesis) {
      const utter = new SpeechSynthesisUtterance(reply);
      utter.rate = 1.05;
      utter.onend = () => setAiState('idle');
      window.speechSynthesis.speak(utter);
    } else {
      setTimeout(() => setAiState('idle'), 2500);
    }
  };

  return (
    <div className="h-full flex flex-col p-6 space-y-6 overflow-y-auto">
      {/* Sub-navigation */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
        <div>
          <div className="flex items-center space-x-2">
            <Mic className="w-5 h-5 text-cyan-neon" />
            <h2 className="text-xl font-bold tracking-wide text-slate-100">
              VOICE & SOUL <span className="text-xs font-mono text-cyan-neon font-normal">/ LIVING OPERATING CORE</span>
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Real-time visual orb pulse, personality tuning & local SQLite context inspector.
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-void-card p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveSubTab('orb')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono transition ${
              activeSubTab === 'orb' ? 'bg-cyan-neon/20 text-cyan-neon border border-cyan-neon/30' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Voice Orb Core
          </button>
          <button
            onClick={() => setActiveSubTab('soul')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono transition ${
              activeSubTab === 'soul' ? 'bg-purple-electric/20 text-purple-electric border border-purple-electric/30' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Soul Tuner
          </button>
          <button
            onClick={() => setActiveSubTab('memory')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono transition ${
              activeSubTab === 'memory' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            SQLite Memory
          </button>
        </div>
      </div>

      {/* Main View Switcher */}
      {activeSubTab === 'soul' ? (
        <SoulTuner />
      ) : activeSubTab === 'memory' ? (
        <MemoryManager />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center flex-1">
          {/* Central Animated Orb */}
          <div className="lg:col-span-7 flex flex-col items-center justify-center p-8 bg-void-card/60 border border-slate-800/80 rounded-3xl relative overflow-hidden min-h-[440px]">
            {/* Grid Pattern */}
            <div className="absolute inset-0 cyber-grid opacity-30 pointer-events-none" />

            {/* Glowing Orb */}
            <div className="relative z-10 flex items-center justify-center my-6">
              {/* Outer Glow Ring */}
              <div
                className={`w-48 h-48 rounded-full flex items-center justify-center transition-all duration-700 ${
                  aiState === 'listening'
                    ? 'border-2 border-cyan-neon shadow-neon-cyan animate-orb scale-105'
                    : aiState === 'thinking'
                    ? 'border-2 border-purple-electric shadow-neon-purple animate-pulse'
                    : aiState === 'speaking'
                    ? 'border-2 border-pink-500 shadow-lg animate-bounce'
                    : 'border border-slate-700 bg-slate-900/40'
                }`}
              >
                {/* Inner Core */}
                <div
                  className={`w-36 h-36 rounded-full flex flex-col items-center justify-center transition-all duration-500 ${
                    aiState === 'listening'
                      ? 'bg-gradient-to-tr from-cyan-neon to-purple-electric text-void'
                      : aiState === 'thinking'
                      ? 'bg-gradient-to-tr from-purple-electric to-pink-500 text-white'
                      : aiState === 'speaking'
                      ? 'bg-gradient-to-tr from-pink-500 to-cyan-neon text-void'
                      : 'bg-void-light border border-slate-800 text-slate-400'
                  }`}
                >
                  <Sparkles className="w-8 h-8 mb-1 animate-pulse" />
                  <span className="text-[10px] font-mono uppercase font-bold tracking-widest">
                    {aiState}
                  </span>
                </div>
              </div>
            </div>

            {/* Real-time Waveform Canvas */}
            <div className="w-full max-w-md h-16 relative z-10 my-2">
              <canvas ref={canvasRef} width={450} height={64} className="w-full h-full" />
            </div>

            {/* Mic Toggle Button */}
            <div className="relative z-10 flex items-center space-x-4 mt-4">
              <button
                onClick={toggleListening}
                className={`flex items-center space-x-2.5 px-6 py-3 rounded-2xl font-bold text-sm tracking-wide transition-all shadow-xl ${
                  isListening
                    ? 'bg-red-500 text-white hover:bg-red-600 shadow-red-500/30'
                    : 'bg-gradient-to-r from-cyan-neon to-purple-electric text-void hover:opacity-90 shadow-neon-cyan'
                }`}
              >
                {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                <span>{isListening ? 'Halt Listening' : 'Activate Voice Core'}</span>
              </button>
            </div>
          </div>

          {/* Right Side Directive Console */}
          <div className="lg:col-span-5 flex flex-col space-y-4">
            {/* Live Transcript Box */}
            <div className="bg-void-card border border-slate-800/80 rounded-2xl p-5 flex flex-col space-y-2">
              <span className="text-[10px] font-mono text-cyan-neon uppercase tracking-wider flex items-center">
                <Terminal className="w-3.5 h-3.5 mr-1" /> Vocal Input Stream
              </span>
              <p className="text-xs text-slate-300 font-mono bg-void-light/70 p-3 rounded-xl border border-slate-800 min-h-[50px]">
                {transcript || 'Awaiting sound wave input...'}
              </p>
            </div>

            {/* AI Synthesized Response Box */}
            <div className="bg-void-card border border-slate-800/80 rounded-2xl p-5 flex flex-col space-y-2">
              <span className="text-[10px] font-mono text-purple-electric uppercase tracking-wider flex items-center">
                <Volume2 className="w-3.5 h-3.5 mr-1" /> Core Acoustic Output
              </span>
              <p className="text-xs text-slate-100 bg-void-light/70 p-3 rounded-xl border border-slate-800 min-h-[80px] leading-relaxed font-sans">
                {aiResponse}
              </p>
            </div>

            {/* Quick Voice Commands Cheat Sheet */}
            <div className="bg-void-card/60 border border-slate-800/80 rounded-2xl p-4">
              <span className="text-[10px] font-mono text-slate-400 uppercase mb-2 block">
                Quick Tested Voice Commands
              </span>
              <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                {[
                  'Open calculator',
                  'Open notepad',
                  'Navigate to D drive',
                  'Task Alice to research',
                ].map((cmd) => (
                  <button
                    key={cmd}
                    onClick={() => {
                      setTranscript(cmd);
                      processVoiceCommand(cmd);
                    }}
                    className="p-2 rounded-lg bg-void-light border border-slate-800 hover:border-cyan-neon/40 text-slate-300 hover:text-cyan-neon text-left transition flex items-center justify-between"
                  >
                    <span className="truncate">{cmd}</span>
                    <ArrowUpRight className="w-3 h-3 ml-1 opacity-60" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

