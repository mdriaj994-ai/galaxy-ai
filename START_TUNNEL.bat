@echo off
chcp 65001 >nul
title JARVIS Voice PC Control - Cloudflare Tunnel
color 0a
echo ========================================================
echo    🌐 JARVIS REMOTE TUNNEL (Internet Access)
echo ========================================================
echo.
echo [*] Exposing JARVIS to the Internet...
echo.
cd /d "%~dp0"
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --config "cloudflared_jarvis.yml" --url http://127.0.0.1:5000
pause

