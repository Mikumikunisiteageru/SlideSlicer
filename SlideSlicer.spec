# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['SlideSlicer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_ssl', '_socket', 'unicodedata', '_lzma', '_bz2', '_hashlib', 'select'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

to_keep = []
to_exclude = {
    'Qt5DBus.dll', 'Qt5Network.dll', 'Qt5Qml.dll', 'Qt5QmlModels', 'Qt5Quick.dll', 'Qt5Svg.dll', 'Qt5WebSockets.dll', 
    'qgif.dll', 'qicns.dll', 'qico.dll', 'qjpeg.dll', 'qsvg.dll', 'qtga.dll', 'qtiff.dll', 'qwbmp.dll', 'qwebp.dll',
    'qsvgicon.dll',
    'opengl32sw.dll', 'd3dcompiler_47.dll', 
    'ucrtbase.dll'
}
for (dest, source, kind) in a.binaries:
    if os.path.split(dest)[1] in to_exclude:
        continue
    to_keep.append((dest, source, kind))
a.binaries = to_keep

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SlideSlicer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['qwindows.dll'],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
