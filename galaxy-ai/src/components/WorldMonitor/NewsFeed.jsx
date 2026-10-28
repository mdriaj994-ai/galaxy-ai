import React, { useState, useEffect } from 'react';
import { Newspaper, AlertCircle, Radio, ExternalLink, RefreshCw } from 'lucide-react';

export default function NewsFeed() {
  const [feeds, setFeeds] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchFeeds = async () => {
    setLoading(true);
    if (window.galaxyBridge?.getGlobalFeeds) {
      try {
        const data = await window.galaxyBridge.getGlobalFeeds();
        setFeeds(data || []);
      } catch (e) {
        console.warn('Feed fetch error:', e);
      }
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchFeeds();
  }, []);

  const urgencyStyles = {
    HIGH: 'bg-red-500/20 text-red-400 border-red-500/30',
    WATCH: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    INFO: 'bg-cyan-neon/15 text-cyan-neon border-cyan-neon/30',
    NORMAL: 'bg-slate-800 text-slate-300 border-slate-700',
  };

  return (
    <div className="bg-void-card border border-slate-800/80 rounded-2xl p-5 flex flex-col space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Radio className="w-4 h-4 text-purple-electric animate-pulse" />
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
            GLOBAL CYBER INTELLIGENCE FEED
          </h3>
        </div>
        <button
          onClick={fetchFeeds}
          className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-100 transition"
          title="Reload Feeds"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1">
        {feeds.map((feed) => (
          <div
            key={feed.id}
            className="p-3 rounded-xl bg-void-light/60 border border-slate-800/80 hover:border-slate-700 transition"
          >
            <div className="flex items-center justify-between text-[10px] font-mono mb-1.5">
              <span className="text-cyan-neon font-bold tracking-wider">{feed.source}</span>
              <span className={`px-2 py-0.5 rounded border font-bold ${urgencyStyles[feed.urgency] || urgencyStyles.NORMAL}`}>
                {feed.urgency}
              </span>
            </div>
            <p className="text-xs text-slate-200 font-sans leading-relaxed">{feed.headline}</p>
            <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono mt-2">
              <span>{feed.region}</span>
              <span>{feed.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

