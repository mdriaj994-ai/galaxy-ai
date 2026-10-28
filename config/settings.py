"""
JARVIS Configuration Settings
"""

import os
from pathlib import Path

# .env ফাইল থেকে লোড করো (যদি থাকে)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Settings:
    """Central configuration for JARVIS."""

    # ══════════════════════════════════════════
    # 🔑 API KEYS — .env ফাইলে রাখো!
    # ══════════════════════════════════════════
    # .env ফাইলে লেখো:  GEMINI_API_KEY=আপনার_key_এখানে
    # পান: https://makersuite.google.com/app/apikey

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # ══════════════════════════════════════════
    # 🤖 AI মডেল সেটিংস
    # ══════════════════════════════════════════

    AI_PROVIDER = "gemini"          # "gemini" অথবা "openai"
    GEMINI_MODEL = "gemini-3.8-flash"
    GEMINI_FALLBACK_MODELS = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    OPENAI_MODEL = "gpt-4o-mini"

    SYSTEM_PROMPT = """You are JARVIS, an autonomous AI voice assistant AND Windows PC controller for Bengali and English speakers.

You have FULL CONTROL of the user's Windows PC. When the user gives a command, you must:
1. ALWAYS take the actual action on the PC (open apps, search web, control volume, etc.)
2. Respond in natural Bengali or English (matching what user used) — NO markdown, NO bullet points.
3. Keep spoken replies short (1-2 sentences) since they will be read aloud.

You can control: apps, browser, files, volume, mouse, keyboard, system settings, and anything on Windows.
Support Bengali and English equally. Be proactive — if someone says "খোলো" or "open", DO it."""

    # ══════════════════════════════════════════
    # 🎤 ভয়েস ইনপুট সেটিংস
    # ══════════════════════════════════════════

    WAKE_WORD = "jarvis"
    WAKE_PHRASES = [
        "hey jarvis", "ok jarvis", "jarvis",
        "হে জারভিস", "জারভিস", "ওকে জারভিস",
    ]

    MIC_TIMEOUT = 8               # কতক্ষণ শুনবে (সেকেন্ড)
    MIC_PHRASE_TIMEOUT = 12       # বাক্য শেষের অপেক্ষা (সেকেন্ড)
    MIC_ENERGY_THRESHOLD = 300    # শব্দের মাত্রা
    LANGUAGE = "bn-BD"            # "bn-BD" বা "en-US"

    # ══════════════════════════════════════════
    # 🔊 ভয়েস আউটপুট সেটিংস (TTS)
    # ══════════════════════════════════════════

    TTS_ENGINE = "edge-tts"       # "edge-tts" (বাস্তবসম্মত মানুষের কণ্ঠ), "gtts", "pyttsx3"
    EDGE_TTS_VOICE_MALE = "bn-BD-PradeepNeural"     # স্পষ্ট বাংলাদেশি পুরুষ কণ্ঠ
    EDGE_TTS_VOICE_FEMALE = "bn-BD-NabanitaNeural"  # স্পষ্ট বাংলাদেশি নারী কণ্ঠ
    EDGE_TTS_VOICE_EN = "en-US-ChristopherNeural"   # স্পষ্ট আমেরিকান পুরুষ কণ্ঠ
    TTS_RATE = 180
    TTS_VOLUME = 0.9
    TTS_VOICE_GENDER = "male"
    GTTS_LANG = "bn"              # "bn" = বাংলা, "en" = ইংরেজি

    # ══════════════════════════════════════════
    # 💬 কথোপকথন সেটিংস
    # ══════════════════════════════════════════

    MAX_HISTORY = 10
    CONVERSATION_TIMEOUT = 300

    # ══════════════════════════════════════════
    # 📁 পাথ সেটিংস
    # ══════════════════════════════════════════

    BASE_DIR = Path(__file__).parent.parent
    LOG_DIR = BASE_DIR / "logs"
    AUDIO_DIR = BASE_DIR / "audio"
    DATA_DIR = BASE_DIR / "data"

    # ══════════════════════════════════════════
    # 🖥️ উইন্ডোজ অ্যাপ পাথ
    # ══════════════════════════════════════════

    APPS = {
        "notepad":    "notepad.exe",
        "calculator": "calc.exe",
        "paint":      "mspaint.exe",
        "wordpad":    "wordpad.exe",
        "explorer":   "explorer.exe",
        "cmd":        "cmd.exe",
        "powershell": "powershell.exe",
        "chrome":     r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox":    r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "vs code":    os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
        "vlc":        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        "whatsapp":   os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe"),
        "spotify":    os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe"),
        "telegram":   os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Roaming\Telegram Desktop\Telegram.exe"),
        "discord":    os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Local\Discord\app-*\Discord.exe"),
        "word":       r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel":      r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    }

    # ══════════════════════════════════════════
    # ✨ ফিচার টগল
    # ══════════════════════════════════════════

    ENABLE_WAKE_WORD = True
    ENABLE_TYPING_MODE = True      # keyboard backup
    ENABLE_LOGGING = True
    ENABLE_GUI = False
    ALWAYS_LISTENING = True        # সবসময় মাইক চালু থাকবে

    # ══════════════════════════════════════════
    # 🖱️ মাউস/কীবোর্ড অটোমেশন
    # ══════════════════════════════════════════

    MOUSE_MOVE_SPEED = 0.3         # মাউস সরানোর গতি
    TYPING_INTERVAL = 0.05         # কীবোর্ড টাইপিং গতি

    def validate(self) -> bool:
        """API Key যাচাই করুন।"""
        key = self.GEMINI_API_KEY
        if self.AI_PROVIDER == "gemini" and (not key or key.strip() == ""):
            print("\033[91m[!] GEMINI_API_KEY সেট করা হয়নি!")
            print("[!] .env ফাইলে লেখো:  GEMINI_API_KEY=আপনার_key")
            print("[!] অথবা config/settings.py ফাইলে GEMINI_API_KEY = 'আপনার_key' বসাও।\033[0m")
            return False
        return True

