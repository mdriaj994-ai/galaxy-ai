@echo off
chcp 65001 >nul
title JARVIS Pure Desktop Voice Assistant (No Browser Needed)
color 0a
echo ========================================================
echo    🎤 JARVIS HANDS-FREE DESKTOP VOICE CONTROLLER
echo ========================================================
echo.
echo [*] কোন ব্রাউজার লাগবে না!
echo [*] অলওয়েজ শুনবে, মুখে বললেই চোখের সামনে সব কাজ হবে:
echo     - "ফেসবুক খোলো", "আমার নাম্বার ০১৭...", "পাসওয়ার্ড ...", "লগইন করো"
echo     - "ক্যালকুলেটর খোলো", "হিসাব করো ১০০ গুণ ২ প্লাস ৩"
echo     - "এন্টিগ্র্যাভিটি খোলো", "চ্যাট বক্সে লেখো ... এবং পাঠাও"
echo.
cd /d "%~dp0"
python jarvis.py
pause
