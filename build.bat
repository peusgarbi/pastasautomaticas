@echo off

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Compilando GeradorReceitas...
pyinstaller GeradorReceitas.spec

echo.
echo Compilando Updater...
pyinstaller Updater.spec

echo.
echo Build finalizado.
pause
