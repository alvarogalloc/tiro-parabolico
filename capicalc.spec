# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['solver.py','app.py'],
    pathex=[],
    binaries=[],
    datas=[('style.css', '.'),('res', 'res')],
    hiddenimports=['matplotlib', 'numpy'],
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
    name='Capi Calc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='res/icon.png'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='capicalc',
)
app = BUNDLE(
    coll,
    name='Capi Calc.app',
    icon='./res/icon.icns',
    bundle_identifier=None,
)
