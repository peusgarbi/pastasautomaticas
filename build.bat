@echo off

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --icon=assets\icon.ico ^
  --name="GeradorReceitas" ^
  main.py

echo.
echo Build finalizado.
pause
