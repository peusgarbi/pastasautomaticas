# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["updater.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="updater",
    console=False,
    icon="assets/icon.ico",
)
