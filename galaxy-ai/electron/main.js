/**
 * Galaxy AI - Primary Electron Main Process
 * Manages the desktop lifecycle, security sandbox, and IPC handlers.
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const db = require('./backend/db');
const osAutomator = require('./backend/os_automator');
const browserBridge = require('./backend/browser_bridge');

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1100,
    minHeight: 700,
    frame: false,
    backgroundColor: '#0B0E14',
    titleBarStyle: 'hidden',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  const isDev = process.env.NODE_ENV !== 'production' && !app.isPackaged;
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Setup IPC Handlers
function setupIpc() {
  // DB Handlers
  ipcMain.handle('db:get-memories', async () => db.getMemories());
  ipcMain.handle('db:save-memory', async (_, { key, value, category }) => db.saveMemory(key, value, category));
  ipcMain.handle('db:delete-memory', async (_, id) => db.deleteMemory(id));

  ipcMain.handle('db:get-tasks', async (_, agentName) => db.getAgentTasks(agentName));
  ipcMain.handle('db:add-task', async (_, { agent, title, priority, status }) => db.addAgentTask(agent, title, priority, status));
  ipcMain.handle('db:update-task-status', async (_, { id, status }) => db.updateTaskStatus(id, status));

  ipcMain.handle('db:get-logs', async (_, limit) => db.getLogs(limit));
  ipcMain.handle('db:log-event', async (_, { eventType, details }) => db.logEvent(eventType, details));

  ipcMain.handle('db:get-settings', async () => db.getSettings());
  ipcMain.handle('db:save-setting', async (_, { key, value }) => db.saveSetting(key, value));

  // OS Automator Handlers
  ipcMain.handle('os:launch-app', async (_, appName) => osAutomator.launchApp(appName));
  ipcMain.handle('os:open-folder', async (_, targetPath) => osAutomator.openFolder(targetPath));
  ipcMain.handle('os:list-dir', async (_, folderPath) => osAutomator.listDirectory(folderPath));
  ipcMain.handle('os:get-metrics', async () => osAutomator.getSystemMetrics());

  // Browser Bridge Handlers
  ipcMain.handle('browser:fetch-url', async (_, url) => browserBridge.fetchUrl(url));
  ipcMain.handle('browser:get-feeds', async () => browserBridge.getGlobalFeeds());

  // Window Controls
  ipcMain.on('window:minimize', () => mainWindow && mainWindow.minimize());
  ipcMain.on('window:maximize', () => {
    if (!mainWindow) return;
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  });
  ipcMain.on('window:close', () => mainWindow && mainWindow.close());
}

app.whenReady().then(() => {
  setupIpc();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

