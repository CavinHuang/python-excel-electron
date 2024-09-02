# -*- mode: python ; coding: utf-8 -*-

# Get path to Chromium executable
import pyppeteer.chromium_downloader
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# 获取 Chromium 可执行文件的路径
chromium_executable = pyppeteer.chromium_downloader.chromium_executable()

# 获取 Chromium 文件夹的路径（通常是可执行文件的父目录）
chromium_folder = os.path.dirname(chromium_executable)
block_cipher = None

# 添加 Chromium 文件夹到 datas
pyppeteer_files = collect_data_files('pyppeteer')
pyppeteer_files.append((chromium_folder, 'pyppeteer/local-chromium'))


a = Analysis(
    ['./api.py'],
    pathex=[os.path.abspath('../venv/'), chromium_folder],
    binaries=[(chromium_executable, 'chromium')],
    datas=pyppeteer_files,
    hiddenimports=collect_submodules('pyppeteer'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='api',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='api',
)