/**
 * Galaxy AI - Desktop OS Automator
 * Controls local applications, file browsing, and system actions.
 */

const { exec, spawn } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

class OSAutomator {
  constructor() {
    this.platform = os.platform(); // 'win32', 'darwin', 'linux'
  }

  // Launch common desktop apps
  launchApp(appName) {
    return new Promise((resolve, reject) => {
      const name = appName.toLowerCase().trim();
      let cmd = '';

      if (this.platform === 'win32') {
        const appMap = {
          notepad: 'notepad.exe',
          calculator: 'calc.exe',
          calc: 'calc.exe',
          chrome: 'start chrome',
          browser: 'start chrome',
          vscode: 'code',
          code: 'code',
          explorer: 'explorer.exe',
          cmd: 'start cmd.exe',
          terminal: 'start wt.exe || start cmd.exe',
          paint: 'mspaint.exe',
          whatsapp: 'start whatsapp:',
          photoshop: 'start photoshop',
        };

        cmd = appMap[name] || `start "" "${appName}"`;
      } else if (this.platform === 'darwin') {
        cmd = `open -a "${appName}"`;
      } else {
        cmd = `${appName} &`;
      }

      exec(cmd, (err) => {
        if (err) {
          console.warn(`[OSAutomator] Direct launch error, trying fallback for ${name}:`, err.message);
          resolve({ success: false, message: `Could not launch ${appName}: ${err.message}` });
        } else {
          resolve({ success: true, message: `Successfully launched ${appName}` });
        }
      });
    });
  }

  // Open directory in native file explorer
  openFolder(targetPath) {
    return new Promise((resolve) => {
      let resolvedPath = targetPath;
      if (!targetPath || targetPath === 'home') {
        resolvedPath = os.homedir();
      } else if (targetPath.toLowerCase() === 'downloads') {
        resolvedPath = path.join(os.homedir(), 'Downloads');
      } else if (targetPath.toLowerCase() === 'desktop') {
        resolvedPath = path.join(os.homedir(), 'Desktop');
      }

      let cmd = '';
      if (this.platform === 'win32') {
        cmd = `explorer.exe "${resolvedPath}"`;
      } else if (this.platform === 'darwin') {
        cmd = `open "${resolvedPath}"`;
      } else {
        cmd = `xdg-open "${resolvedPath}"`;
      }

      exec(cmd, (err) => {
        if (err) {
          resolve({ success: false, message: `Failed to open ${resolvedPath}` });
        } else {
          resolve({ success: true, path: resolvedPath });
        }
      });
    });
  }

  // List files in a local folder
  listDirectory(folderPath) {
    try {
      const p = folderPath || os.homedir();
      if (!fs.existsSync(p)) {
        return { success: false, message: 'Directory does not exist' };
      }
      const files = fs.readdirSync(p, { withFileTypes: true }).map((dirent) => ({
        name: dirent.name,
        isDirectory: dirent.isDirectory(),
        size: dirent.isDirectory() ? null : fs.statSync(path.join(p, dirent.name)).size,
      }));
      return { success: true, path: p, files: files.slice(0, 50) };
    } catch (err) {
      return { success: false, message: err.message };
    }
  }

  // Get system performance stats
  getSystemMetrics() {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;
    const cpus = os.cpus();

    return {
      platform: this.platform,
      hostname: os.hostname(),
      uptimeHours: Math.round(os.uptime() / 3600),
      cpuModel: cpus[0] ? cpus[0].model : 'Unknown',
      cpuCount: cpus.length,
      memoryTotalGB: (totalMem / 1024 ** 3).toFixed(2),
      memoryUsedGB: (usedMem / 1024 ** 3).toFixed(2),
      memoryUsagePercent: Math.round((usedMem / totalMem) * 100),
      loadAvg: os.loadavg(),
    };
  }
}

module.exports = new OSAutomator();

