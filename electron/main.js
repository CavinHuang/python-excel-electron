const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWindow.loadURL('http://localhost:5173');  // Vite dev server URL

  mainWindow.on('closed', function () {
    mainWindow = null;
  });

  mainWindow.webContents.openDevTools()
}

function startPythonBackend() {
  pythonProcess = spawn('python', ['backend/api.py'], {
    cwd: path.resolve(__dirname, '..'),
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });
}

app.on('ready', () => {
  createWindow();
  startPythonBackend();
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});

app.on('will-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});