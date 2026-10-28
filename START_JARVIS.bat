@echo off
chcp 65001 >nul
title JARVIS Voice PC Control - Active Controller
color 0b
echo ========================================================
echo    🚀 JARVIS PC VOICE CONTROLLER (Active Desktop Mode)
echo ========================================================
echo.
echo [*] Starting JARVIS on your active Windows desktop...
echo [*] Python Server will control your actual screen, apps and windows!
echo.
cd /d "%~dp0"
python server.py
pause

