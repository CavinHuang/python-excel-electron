# -*- mode: python ; coding: utf-8 -*-

# Get path to Chromium executable
import pyppeteer.chromium_downloader
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

chromium_executable = pyppeteer.chromium_downloader.chromium_executable()

block_cipher = None

pyppeteer_files = collect_data_files('pyppeteer')


a = Analysis(
    ['./api.py'],
    pathex=[os.path.abspath('../venv/'), os.path.dirname(chromium_executable)],
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