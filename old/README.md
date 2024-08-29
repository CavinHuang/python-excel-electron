# NODE
Vite uses node: import which is supported in v16.0.0+ and v14.18.0+. v15 does not support this.

## START
``` bash
# main目录
cd main
# 安装 venv
python3 -m venv venv

# mac激活python环境
source venv/bin/activate

# windows激活python环境
venv\Scripts\activate

# 安装 pyinstaller
pip3 install -r requirements.txt （不要翻墙）
# 把 python 代码打包为可执行文件
npm run build-python


# 根目录
# 安装当前依赖
npm i
# 安装前端&electron依赖
npm run install
# 启动项目(前端localhost:3000 & electron)
npm run start

# 构建
npm run build
```


## 网页项目

``` bash
# 进入前端项目
cd renderer

# 安装依赖
npm i

# 开发localhost:3000
npm run dev

# 构建
npm run build
```

## Electron项目 预览和打包都是使用前端构建的文件
``` bash
# 进入前端项目进行构建
cd renderer
npm run build

# 进入electron
cd main

# 安装依赖
npm i

# 预览
npm run electron

# 打包
npm run electron:build
```


# TODO

```bash
# py脚本
区分开发环境直接执行/main/py -> python3 api.py
正式打包才执行/main/py ->  npm run build-python

```


# 项目布局

```
.
├── main                                        // electron项目目录
│   │── build                                     // py打包产物
│   ├── dist                                      // 前端项目打包产物
│   ├── dist_electron                             // electron打包产物（安装应用文件）
│   ├── electron                                  // electron开发目录
│   ├── py                                        // py开发目录
│   ├── pydist                                    // py打包产物
│   └── requirements.txt                          // py依赖项
├── renderer                                      // 前端项目目录
│   │── public                                      // 前端静态资源
│   └── src                                         // 前端页面文件

.

```