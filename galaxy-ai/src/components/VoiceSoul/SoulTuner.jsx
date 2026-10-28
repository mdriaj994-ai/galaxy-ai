import React, { useState, useEffect } from 'react';
import { Sliders, Sparkles, Shield, HeartHandshake, Bot, Save } from 'lucide-react';

export default function SoulTuner() {
  const [traits, setTraits] = useState({
    tonePreset: 'jarvis', // 'jarvis', 'butler', 'companion', 'tactical'
    formality: 85,
    proactiveness: 70,
    empathy: 50,
    creativity: 65,
    humor: 40,
  });

  const [savedNotice, setSavedNotice] = useState(false);

  useEffect(() => {
    const loadSettings = async () => {
      if (window.galaxyBridge?.getSettings) {
        try {
          const s = await window.galaxyBridge.getSettings();
          if (s?.soul_tone) {
            setTraits((prev) => ({ ...prev, tonePreset: s.soul_tone }));
          }
        } catch (e) {
          console.warn('Failed loading soul settings:', e);
        }
      }
    };
    loadSettings();
  }, []);

  const presets = [
    {
      id: 'jarvis',
      name: 'Jarvis Protocol',
      desc: 'Witty, hyper-intelligent, composed, and razor-sharp executive assistant.',
      icon: Bot,
      color: 'border-cyan-neon text-cyan-neon bg-cyan-neon/10',
      values: { formality: 80, proactiveness: 90, empathy: 50, creativity: 75, humor: 65 },
    },
    {
      id: 'butler',
      name: 'Loyal Butler',
      desc: 'Deeply respectful, classical Victorian manners with utmost precision and discretion.',
      icon: Shield,
      color: 'border-purple-electric text-purple-electric bg-purple-electric/10',
      values: { formality: 95, proactiveness: 60, empathy: 70, creativity: 40, humor: 25 },
    },
    {
      id: 'companion',
      name: 'Friendly Companion',
      desc: 'Warm, conversational, empathetic, and encouraging everyday partner.',
      icon: HeartHandshake,
      color: 'border-pink-500 text-pink-400 bg-pink-500/10',
      values: { formality: 40, proactiveness: 80, empathy: 95, creativity: 85, humor: 80 },
    },
  ];

  const applyPreset = (preset) => {
    setTraits({
      tonePreset: preset.id,
      ...preset.values,
    });
  };

  const handleSave = async () => {
    if (window.galaxyBridge?.saveSetting) {
      await window.galaxyBridge.saveSetting('soul_tone', traits.tonePreset);
      await window.galaxyBridge.saveSetting('soul_traits', JSON.stringify(traits));
      await window.galaxyBridge.logEvent('SOUL_TUNER_UPDATE', `Applied soul preset: ${traits.tonePreset}`);
    }
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 2000);
  };

  return (
    <div className="bg-void-card border border-slate-800/80 rounded-2xl p-6 flex flex-col space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-100 flex items-center">
            <Sliders className="w-4 h-4 text-purple-electric mr-2" />
            SOUL TUNER <span className="ml-2 text-xs font-mono text-purple-electric font-normal">/ PERSONALITY MATRIX</span>
          </h3>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Fine-tune the neural personality weights of your local operating core.
          </p>
        </div>
        <button
          onClick={handleSave}
          className="flex items-center space-x-1.5 bg-purple-electric hover:bg-purple-electric/90 text-white font-bold text-xs px-3.5 py-1.5 rounded-lg transition shadow-neon-purple"
        >
          <Save className="w-3.5 h-3.5" />
          <span>{savedNotice ? 'Saved!' : 'Save Traits'}</span>
        </button>
      </div>

      {/* Preset Archetypes */}
      <div>
        <label className="block text-xs font-mono text-slate-400 uppercase mb-3">Tone Archetypes</label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {presets.map((p) => {
            const Icon = p.icon;
            const isSelected = traits.tonePreset === p.id;
            return (
              <button
                key={p.id}
                onClick={() => applyPreset(p)}
                className={`p-4 rounded-xl border text-left transition-all duration-200 ${
                  isSelected
                    ? `${p.color} shadow-lg scale-[1.02]`
                    : 'border-slate-800 bg-void-light/60 text-slate-400 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center space-x-2 mb-2">
                  <Icon className="w-4 h-4" />
                  <span className="text-xs font-bold">{p.name}</span>
                </div>
                <p className="text-[11px] text-slate-400 font-sans leading-relaxed">{p.desc}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Sliders */}
      <div className="space-y-4 pt-2">
        <label className="block text-xs font-mono text-slate-400 uppercase">Core Neural Sliders</label>

        {[
          { key: 'formality', label: 'Formality & Protocol', low: 'Casual', high: 'Classical High Butler' },
          { key: 'proactiveness', label: 'Proactive Autonomy', low: 'Wait for prompt', high: 'Anticipate next action' },
          { key: 'empathy', label: 'Empathetic Warmth', low: 'Pure Logic & Math', high: 'Deep Emotional Resonance' },
          { key: 'creativity', label: 'Creative Deviation', low: 'Strict Deterministic', high: 'Expansive Imagination' },
        ].map((s) => (
          <div key={s.key} className="bg-void-light/50 p-3 rounded-xl border border-slate-800/60">
            <div className="flex justify-between items-center text-xs mb-1.5 font-mono">
              <span className="text-slate-300 font-semibold">{s.label}</span>
              <span className="text-cyan-neon font-bold">{traits[s.key]}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={traits[s.key]}
              onChange={(e) => setTraits({ ...traits, [s.key]: Number(e.target.value) })}
              className="w-full accent-cyan-neon h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
              <span>{s.low}</span>
              <span>{s.high}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

