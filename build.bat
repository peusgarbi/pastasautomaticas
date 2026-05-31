@echo off

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

pyinstaller GeradorReceitas.spec

echo.
echo Build finalizado.
pause
