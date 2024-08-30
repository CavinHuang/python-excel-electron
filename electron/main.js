const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

const NODE_ENV = process.env.NODE_ENV
let pyProc = null


function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  /**
   * 打开开发工具
   * 加载 index.html
   */
  if (NODE_ENV === "development") {
    mainWindow.loadURL('http://localhost:3000')
  } else {
    mainWindow.loadURL(`file://${path.join(app.getAppPath(), '/frontend/dist/index.html')}`);
  }

  mainWindow.on('closed', function () {
    mainWindow = null;
  });

  mainWindow.webContents.openDevTools()
}

function startDevPythonBackend() {
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

function startProPythonBackend() {
  let port = '4242'

  const appPath = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked') : app.getAppPath();
  const pythonExecPath = path.join(appPath, 'backend/pydist/api/api');

  pyProc = require('child_process').execFile(pythonExecPath, [port], (error, stdout, stderr) => {
    if (error) {
      throw error;
    }
    console.log(stdout);
  })

  pyProc.on('error', (error) => {
    console.error(`Python process error: ${error.message}`);
  });

  pyProc.stdout?.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pyProc.stderr?.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  if (pyProc != null) {
    console.log('child process success')
  }
}

function startPythonBackend() {
  if (NODE_ENV === "development") {
    startDevPythonBackend();
  } else {
    startProPythonBackend();
  }
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
  if (pyProc) {
    pyProc.kill();
  }
});