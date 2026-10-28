/**
 * Galaxy AI - Local SQLite Database & Storage Engine
 * Local-first memory persistence with automatic fallback to JSON store.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const DATA_DIR = path.join(os.homedir(), '.galaxy-ai');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const DB_PATH = path.join(DATA_DIR, 'galaxy_memory.sqlite');
const FALLBACK_PATH = path.join(DATA_DIR, 'galaxy_memory.json');

class DatabaseEngine {
  constructor() {
    this.useSqlite = false;
    this.sqlite = null;
    this.fallbackData = {
      memories: [],
      agent_tasks: [],
      logs: [],
      settings: {
        theme: 'cyberpunk',
        soul_tone: 'jarvis',
        voice_rate: 1.0,
        license_active: true,
        user_name: 'Commander',
      },
    };

    this.init();
  }

  init() {
    try {
      const Database = require('better-sqlite3');
      this.sqlite = new Database(DB_PATH);
      this.sqlite.pragma('journal_mode = WAL');
      this.useSqlite = true;
      this.setupTables();
      console.log('[Galaxy DB] SQLite initialized at:', DB_PATH);
    } catch (err) {
      console.warn('[Galaxy DB] better-sqlite3 not compiled, using persistent JSON engine:', err.message);
      this.loadFallback();
    }
  }

  setupTables() {
    this.sqlite.exec(`
      CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        value TEXT,
        category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS agent_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent TEXT,
        title TEXT,
        status TEXT,
        priority TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        details TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
      );
    `);

    // Seed default settings if empty
    const check = this.sqlite.prepare('SELECT COUNT(*) as count FROM settings').get();
    if (check.count === 0) {
      const stmt = this.sqlite.prepare('INSERT INTO settings (key, value) VALUES (?, ?)');
      stmt.run('theme', 'cyberpunk');
      stmt.run('soul_tone', 'jarvis');
      stmt.run('user_name', 'Commander');
      stmt.run('license_active', 'true');
    }
  }

  loadFallback() {
    if (fs.existsSync(FALLBACK_PATH)) {
      try {
        const raw = fs.readFileSync(FALLBACK_PATH, 'utf8');
        this.fallbackData = JSON.parse(raw);
      } catch (e) {
        console.error('[Galaxy DB] Failed reading fallback JSON:', e);
      }
    } else {
      this.saveFallback();
    }
  }

  saveFallback() {
    try {
      fs.writeFileSync(FALLBACK_PATH, JSON.stringify(this.fallbackData, null, 2), 'utf8');
    } catch (e) {
      console.error('[Galaxy DB] Failed writing fallback JSON:', e);
    }
  }

  // --- MEMORIES API ---
  getMemories() {
    if (this.useSqlite) {
      return this.sqlite.prepare('SELECT * FROM memories ORDER BY created_at DESC').all();
    }
    return this.fallbackData.memories || [];
  }

  saveMemory(key, value, category = 'general') {
    if (this.useSqlite) {
      const stmt = this.sqlite.prepare(`
        INSERT INTO memories (key, value, category) VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, category=excluded.category
      `);
      return stmt.run(key, value, category);
    }
    const idx = this.fallbackData.memories.findIndex((m) => m.key === key);
    if (idx >= 0) {
      this.fallbackData.memories[idx] = { key, value, category, created_at: new Date().toISOString() };
    } else {
      this.fallbackData.memories.unshift({ id: Date.now(), key, value, category, created_at: new Date().toISOString() });
    }
    this.saveFallback();
    return true;
  }

  deleteMemory(id) {
    if (this.useSqlite) {
      return this.sqlite.prepare('DELETE FROM memories WHERE id = ?').run(id);
    }
    this.fallbackData.memories = this.fallbackData.memories.filter((m) => m.id !== id);
    this.saveFallback();
    return true;
  }

  // --- AGENT TASKS API ---
  getAgentTasks(agentName = null) {
    if (this.useSqlite) {
      if (agentName) {
        return this.sqlite.prepare('SELECT * FROM agent_tasks WHERE agent = ? ORDER BY created_at DESC').all(agentName);
      }
      return this.sqlite.prepare('SELECT * FROM agent_tasks ORDER BY created_at DESC').all();
    }
    if (agentName) {
      return this.fallbackData.agent_tasks.filter((t) => t.agent.toLowerCase() === agentName.toLowerCase());
    }
    return this.fallbackData.agent_tasks;
  }

  addAgentTask(agent, title, priority = 'Medium', status = 'Working') {
    if (this.useSqlite) {
      const stmt = this.sqlite.prepare('INSERT INTO agent_tasks (agent, title, status, priority) VALUES (?, ?, ?, ?)');
      return stmt.run(agent, title, status, priority);
    }
    const newTask = {
      id: Date.now(),
      agent,
      title,
      status,
      priority,
      created_at: new Date().toISOString(),
    };
    this.fallbackData.agent_tasks.unshift(newTask);
    this.saveFallback();
    return newTask;
  }

  updateTaskStatus(id, status) {
    if (this.useSqlite) {
      return this.sqlite.prepare('UPDATE agent_tasks SET status = ? WHERE id = ?').run(status, id);
    }
    const t = this.fallbackData.agent_tasks.find((task) => task.id === id);
    if (t) t.status = status;
    this.saveFallback();
    return true;
  }

  // --- LOGS API ---
  logEvent(eventType, details) {
    if (this.useSqlite) {
      return this.sqlite.prepare('INSERT INTO logs (event_type, details) VALUES (?, ?)').run(eventType, typeof details === 'object' ? JSON.stringify(details) : details);
    }
    this.fallbackData.logs.unshift({
      id: Date.now(),
      event_type: eventType,
      details: typeof details === 'object' ? JSON.stringify(details) : details,
      timestamp: new Date().toISOString(),
    });
    if (this.fallbackData.logs.length > 200) this.fallbackData.logs.pop();
    this.saveFallback();
  }

  getLogs(limit = 50) {
    if (this.useSqlite) {
      return this.sqlite.prepare('SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?').all(limit);
    }
    return (this.fallbackData.logs || []).slice(0, limit);
  }

  // --- SETTINGS API ---
  getSettings() {
    if (this.useSqlite) {
      const rows = this.sqlite.prepare('SELECT * FROM settings').all();
      const obj = {};
      rows.forEach((r) => { obj[r.key] = r.value; });
      return obj;
    }
    return this.fallbackData.settings;
  }

  saveSetting(key, value) {
    if (this.useSqlite) {
      return this.sqlite.prepare('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(key, String(value));
    }
    this.fallbackData.settings[key] = value;
    this.saveFallback();
    return true;
  }
}

module.exports = new DatabaseEngine();

