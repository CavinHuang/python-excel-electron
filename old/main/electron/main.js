// 控制应用生命周期和创建原生浏览器窗口的模组
const { app, BrowserWindow } = require('electron')
const path = require('path')

const NODE_ENV = process.env.NODE_ENV
let pyProc = null

function createWindow () {
  // 创建浏览器窗口
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  /**
   * 打开开发工具
   * 加载 index.html
   */
  if (NODE_ENV === "development") {
    mainWindow.loadURL('http://localhost:3000')
  } else {
    mainWindow.loadURL(`file://${path.join(app.getAppPath(), '/dist/index.html')}`);
  }
  mainWindow.webContents.openDevTools()

}

const createPyProc = () => {
  let port = '4242'

  const appPath = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked') : app.getAppPath();
  const pythonExecPath = path.join(appPath, 'pydist/api/api');
  const pythonExecPathDev = `python ${path.join(appPath, 'py/api.py')}`;

  // let script = path.join(app.getAppPath(), '/pydist/api/api')

  let pythonService = pythonExecPathDev

  if (NODE_ENV === "production") {
    pythonService = pythonExecPath
  }

  console.log("Python script path: " + pythonService);

  pyProc = require('child_process').execFile(pythonService, [port], (error, stdout, stderr) => {
    if (error) {
      throw error;
    }
    console.log(stdout);
  })

  pyProc.on('error', (error) => {
    console.error(`Python process error: ${error.message}`);
  });

  pyProc.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pyProc.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  if (pyProc != null) {
    console.log('child process success')
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
}


// 这段程序将会在 Electron 结束初始化
// 和创建浏览器窗口的时候调用
// 部分 API 在 ready 事件触发后才能使用。
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // 通常在 macOS 上，当点击 dock 中的应用程序图标时，如果没有其他
    // 打开的窗口，那么程序会重新创建一个窗口。
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('ready', createPyProc)

// 除了 macOS 外，当所有窗口都被关闭的时候退出程序。 因此，通常对程序和它们在
// 任务栏上的图标来说，应当保持活跃状态，直到用户使用 Cmd + Q 退出。
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

app.on('will-quit', exitPyProc)

// 在这个文件中，你可以包含应用程序剩余的所有部分的代码，
// 也可以拆分成几个文件，然后用 require 导入。