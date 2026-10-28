/**
 * Galaxy AI - Secure Electron Preload IPC Bridge
 * Exposes system automations, SQLite DB, and OS metrics safely to the renderer.
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('galaxyBridge', {
  // DB
  getMemories: () => ipcRenderer.invoke('db:get-memories'),
  saveMemory: (key, value, category) => ipcRenderer.invoke('db:save-memory', { key, value, category }),
  deleteMemory: (id) => ipcRenderer.invoke('db:delete-memory', id),

  getAgentTasks: (agentName) => ipcRenderer.invoke('db:get-tasks', agentName),
  addAgentTask: (agent, title, priority, status) => ipcRenderer.invoke('db:add-task', { agent, title, priority, status }),
  updateTaskStatus: (id, status) => ipcRenderer.invoke('db:update-task-status', { id, status }),

  getLogs: (limit) => ipcRenderer.invoke('db:get-logs', limit),
  logEvent: (eventType, details) => ipcRenderer.invoke('db:log-event', { eventType, details }),

  getSettings: () => ipcRenderer.invoke('db:get-settings'),
  saveSetting: (key, value) => ipcRenderer.invoke('db:save-setting', { key, value }),

  // OS Automator
  launchApp: (appName) => ipcRenderer.invoke('os:launch-app', appName),
  openFolder: (targetPath) => ipcRenderer.invoke('os:open-folder', targetPath),
  listDirectory: (folderPath) => ipcRenderer.invoke('os:list-dir', folderPath),
  getSystemMetrics: () => ipcRenderer.invoke('os:get-metrics'),

  // Browser Bridge
  fetchUrl: (url) => ipcRenderer.invoke('browser:fetch-url', url),
  getGlobalFeeds: () => ipcRenderer.invoke('browser:get-feeds'),

  // Window Controls
  minimizeWindow: () => ipcRenderer.send('window:minimize'),
  maximizeWindow: () => ipcRenderer.send('window:maximize'),
  closeWindow: () => ipcRenderer.send('window:close'),
});

