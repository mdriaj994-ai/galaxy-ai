# 🌌 Galaxy AI
> **Local-First Desktop & Mobile AI Assistant Application Framework**

Built with **Electron.js**, **React 18**, **Tailwind CSS**, and **Local SQLite** with zero cloud runtime dependencies.

---

## 🏗️ Architecture & Modules

### 1. 👥 Agent Town (Virtual Office)
- **Alice** (Researcher)
- **Bob** (Developer)
- **Carol** (Creative Director)
- **Dave** (Data Analyst)
- Live status cycles: `Idle`, `Working`, `Collaborating`.
- Direct face-to-face task assignment modals with priority queues stored in SQLite.

### 2. 🔮 Voice & Soul Engine
- Central animated AI Orb with reactive audio frequency waveform.
- **Soul Tuner:** Personality trait sliders (Jarvis protocol, Victorian Butler, Friendly Companion).
- **SQLite Memory Inspector:** Add, search, and delete local user context without sending data to external clouds.

### 3. 🌐 World Monitor (Global Command Radar)
- 3D rotating wireframe globe on HTML5 Canvas.
- Multi-timezone live UTC clocks (London, New York, Tokyo, Dhaka, Zulu).
- Active global telemetry nodes & real-time cyber news feed parser.

### 4. 📐 Diagram Generation Engine
- Interactive draggable canvas generating **Mind Maps**, **Workflows**, and **System Architecture Diagrams**.
- Smooth curved bezier connector lines, node title editing, and JSON export.

### 5. 📱 Android Sync & Mobile Companion
- Live Android smartphone simulator mockup.
- React Native companion codebase inside `/mobile` with native Android intent services (`DeviceControl.js`) for launching YouTube, Facebook, Alarms, and camera.
- PDF & image document analyzer with local extraction.

---

## ⚡ Quick Start

### Run Desktop App in Browser Mode (Fast Dev Preview):
```bash
cd galaxy-ai
npm install
npm run dev
```
Navigate to `http://localhost:5173`.

### Run Desktop App with Full Electron Engine:
```bash
cd galaxy-ai
npm run electron:dev
```

### Run Mobile Companion (React Native / Expo):
```bash
cd galaxy-ai/mobile
npm install
npm start
```

