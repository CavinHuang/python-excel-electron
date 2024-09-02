# NODE
Vite uses node: import which is supported in v16.0.0+ and v14.18.0+. v15 does not support this.
/Users/cavinhuang/Library/Application Support/pyppeteer/local-chromium/1181205
## START
``` bash
# 根目录

# 安装 venv
python -m venv venv

# mac激活python环境
source venv/bin/activate

# windows激活python环境
venv\Scripts\activate

# 安装 pyinstaller
pip install -r requirements.txt （不要翻墙）
# 把 python 代码打包为可执行文件
pnpm run build-python

# 安装当前依赖
pnpm i
# 安装前端&electron依赖
pnpm run install
# 启动项目(前端localhost:3000 & electron)
pnpm run start

# 构建
pnpm run build
```


## 网页项目

``` bash
# 进入前端项目
cd renderer

# 安装依赖
npm i

# 开发localhost:3000
pnpm run dev

# 构建
pnpm run build
```

## Electron项目 预览和打包都是使用前端构建的文件
``` bash
# 进入前端项目进行构建
cd frontend
pnpm run build

# 进入electron
cd main

# 安装依赖
pnpm i

# 预览
pnpm run electron

# 打包
pnpm run electron:build
```
