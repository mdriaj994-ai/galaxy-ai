import React, { useState } from 'react';
import { 
  Send, 
  Paperclip, 
  Mic, 
  FileText, 
  Image as ImageIcon, 
  Smartphone, 
  CheckCircle2, 
  Play, 
  Bell, 
  Share2 
} from 'lucide-react';

export default function VoiceChatPanel({ onTriggerIntent }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: 'Galaxy AI Mobile Core linked. Ready to execute device intents, analyze files, or transcribe audio.',
      time: '12:00 PM',
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [analyzingFile, setAnalyzingFile] = useState(false);

  const handleSend = (textToSend = null) => {
    const text = textToSend || inputText;
    if (!text.trim()) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputText('');

    // Process mobile intent
    setTimeout(() => {
      let reply = `Understood: "${text}". Action logged on Android companion.`;
      const low = text.toLowerCase();

      if (low.includes('youtube')) {
        reply = 'Launching YouTube App via Android Intent: com.google.android.youtube';
        onTriggerIntent?.('YouTube');
      } else if (low.includes('facebook') || low.includes('fb')) {
        reply = 'Dispatching Facebook intent to Android system.';
        onTriggerIntent?.('Facebook');
      } else if (low.includes('alarm')) {
        reply = 'Setting Android Alarm intent for 07:00 AM.';
        onTriggerIntent?.('Alarm');
      }

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: reply,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    }, 800);
  };

  const handleSimulateFileUpload = (type) => {
    setAnalyzingFile(true);
    setTimeout(() => {
      setAnalyzingFile(false);
      const fileName = type === 'pdf' ? 'Project_Architecture_Doc.pdf' : 'Screenshot_2026.png';
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          sender: 'user',
          text: `Uploaded [${fileName}] for local analysis.`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          file: { name: fileName, type },
        },
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: `[Analyzed ${fileName}]: Document parsed locally. Contains 4 components, SQLite schema definitions, and IPC contracts. Zero anomalies found.`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    }, 1500);
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-void-card/90 border border-slate-800/80 rounded-2xl overflow-hidden p-4">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-1 mb-3">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`max-w-[85%] p-3 rounded-2xl text-xs leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-gradient-to-r from-purple-electric to-cyan-neon text-void font-semibold rounded-tr-none'
                  : 'bg-void-light border border-slate-800 text-slate-200 rounded-tl-none font-sans'
              }`}
            >
              {m.file && (
                <div className="flex items-center space-x-2 mb-1.5 p-1.5 rounded-lg bg-black/20 font-mono text-[10px]">
                  {m.file.type === 'pdf' ? <FileText className="w-3.5 h-3.5" /> : <ImageIcon className="w-3.5 h-3.5" />}
                  <span>{m.file.name}</span>
                </div>
              )}
              <p>{m.text}</p>
            </div>
            <span className="text-[9px] font-mono text-slate-500 mt-1 px-1">{m.time}</span>
          </div>
        ))}

        {analyzingFile && (
          <div className="flex items-center space-x-2 text-xs font-mono text-cyan-neon bg-cyan-neon/10 p-2.5 rounded-xl border border-cyan-neon/30 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-cyan-neon" />
            <span>Parsing file tokens with local embedding extractor...</span>
          </div>
        )}
      </div>

      {/* Quick Intent Shortcut Chips */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-2 border-t border-slate-800/80 pt-2 text-[10px] font-mono">
        <span className="text-slate-500 uppercase">Intents:</span>
        <button
          onClick={() => handleSend('Open YouTube app')}
          className="px-2.5 py-1 rounded-lg bg-void-light border border-slate-800 hover:border-red-500 text-slate-300 hover:text-red-400 whitespace-nowrap flex items-center space-x-1"
        >
          <Play className="w-3 h-3 text-red-500" />
          <span>YouTube</span>
        </button>
        <button
          onClick={() => handleSend('Open Facebook app')}
          className="px-2.5 py-1 rounded-lg bg-void-light border border-slate-800 hover:border-blue-500 text-slate-300 hover:text-blue-400 whitespace-nowrap flex items-center space-x-1"
        >
          <Share2 className="w-3 h-3 text-blue-500" />
          <span>Facebook</span>
        </button>
        <button
          onClick={() => handleSend('Set Alarm for 7 AM')}
          className="px-2.5 py-1 rounded-lg bg-void-light border border-slate-800 hover:border-amber-500 text-slate-300 hover:text-amber-400 whitespace-nowrap flex items-center space-x-1"
        >
          <Bell className="w-3 h-3 text-amber-500" />
          <span>Set Alarm</span>
        </button>
        <button
          onClick={() => handleSimulateFileUpload('pdf')}
          className="px-2.5 py-1 rounded-lg bg-void-light border border-slate-800 hover:border-cyan-neon text-slate-300 hover:text-cyan-neon whitespace-nowrap flex items-center space-x-1"
        >
          <FileText className="w-3 h-3 text-cyan-neon" />
          <span>Analyze PDF</span>
        </button>
        <button
          onClick={() => handleSimulateFileUpload('img')}
          className="px-2.5 py-1 rounded-lg bg-void-light border border-slate-800 hover:border-pink-500 text-slate-300 hover:text-pink-400 whitespace-nowrap flex items-center space-x-1"
        >
          <ImageIcon className="w-3 h-3 text-pink-400" />
          <span>Analyze Image</span>
        </button>
      </div>

      {/* Input Bar */}
      <div className="flex items-center space-x-2 mt-1">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Send voice instruction or prompt to mobile core..."
          className="flex-1 bg-void-light border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 placeholder-slate-500 font-mono focus:outline-none focus:border-cyan-neon"
        />
        <button
          onClick={() => handleSend()}
          className="p-2 rounded-xl bg-cyan-neon hover:bg-cyan-neon/90 text-void font-bold transition shadow-neon-cyan"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

