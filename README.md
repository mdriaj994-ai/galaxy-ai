# 🤖 JARVIS - AI Voice Assistant
### Just A Rather Very Intelligent System | Powered by Google Gemini

```
    ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
    ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
    ██║███████║██████╔╝██║   ██║██║███████╗
██  ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
```

---

## ✨ ফিচার সমূহ

| ক্যাটাগরি | ফিচার |
|-----------|-------|
| 🎤 **ভয়েস** | মাইক্রোফোন থেকে কথা শোনে, কথা বলে |
| 🤖 **AI** | Google Gemini / OpenAI GPT দিয়ে স্মার্ট উত্তর |
| 🌐 **ওয়েব** | Google, YouTube, যেকোনো ওয়েবসাইট খোলে |
| 🖥️ **সিস্টেম** | নোটপ্যাড, ক্যালকুলেটর, Chrome খোলে |
| 🔊 **ভলিউম** | ভলিউম বাড়ায়, কমায়, মিউট করে |
| 📸 **স্ক্রিনশট** | ডেস্কটপ স্ক্রিনশট নেয় |
| ⏰ **তথ্য** | সময়, তারিখ, দিন বলে |
| 🔒 **নিরাপত্তা** | স্ক্রিন লক, শাটডাউন, রিস্টার্ট |
| ⌨️ **টাইপিং মোড** | কীবোর্ড দিয়েও কমান্ড দেওয়া যায় |

---

## 🚀 শুরু করুন (Quick Start)

### ধাপ ১: Python ইনস্টল করুন
Python 3.9+ দরকার। ডাউনলোড করুন: https://python.org

### ধাপ ২: প্রজেক্ট ফোল্ডারে যান
```bash
cd "Voice PC contol"
```

### ধাপ ৩: সেটআপ চালান
```bash
python setup.py
```

### ধাপ ৪: API Key সেট করুন
`config/settings.py` ফাইল খুলুন এবং আপনার Gemini API Key বসান:
```python
GEMINI_API_KEY = "আপনার_gemini_api_key_এখানে"
```

> **Gemini API Key বিনামূল্যে পাওয়া যায়:** https://makersuite.google.com/app/apikey

### ধাপ ৫: JARVIS চালু করুন!
```bash
python jarvis.py
```

---

## 🎯 কমান্ড তালিকা

### 🌐 ওয়েব কমান্ড
```
"search Python tutorial"       → Google এ সার্চ করবে
"youtube Bangla song"          → YouTube এ সার্চ করবে
"open facebook"                → Facebook খুলবে
"open github"                  → GitHub খুলবে
"go to google.com"             → যেকোনো সাইট খুলবে
```

### 🖥️ অ্যাপ কমান্ড
```
"open notepad"                 → নোটপ্যাড খুলবে
"open calculator"              → ক্যালকুলেটর খুলবে
"open chrome"                  → Chrome খুলবে
"open vs code"                 → VS Code খুলবে
"open file explorer"           → ফাইল এক্সপ্লোরার খুলবে
```

### 📅 তথ্য কমান্ড
```
"what time is it"              → সময় বলবে
"what's the date"              → তারিখ বলবে
"what day is it"               → দিন বলবে
"system info"                  → কম্পিউটার তথ্য বলবে
```

### 🔊 ভলিউম কমান্ড
```
"volume up"                    → ভলিউম বাড়াবে
"volume down"                  → ভলিউম কমাবে
"mute"                         → মিউট করবে
```

### 🖥️ সিস্টেম কমান্ড
```
"screenshot"                   → স্ক্রিনশট নেবে
"lock screen"                  → স্ক্রিন লক করবে
"shutdown"                     → কম্পিউটার বন্ধ করবে
"restart"                      → রিস্টার্ট করবে
"sleep"                        → স্লিপ মোডে যাবে
```

### 🤖 AI কমান্ড
```
"tell me about quantum physics" → AI ব্যাখ্যা করবে
"write a Python function"       → কোড লিখবে
"what is machine learning"      → যেকোনো প্রশ্নের উত্তর
"tell me a joke"                → মজার জোকস বলবে
```

### 🎮 মজার কমান্ড
```
"tell me a joke"               → জোকস বলবে
"flip a coin"                  → কয়েন ফ্লিপ করবে
"roll a dice"                  → ডাইস রোল করবে
"calculate 15 * 7"             → গাণিতিক হিসাব
```

### 🔧 নিয়ন্ত্রণ
```
"clear history"                → কথোপকথন মুছবে
"help"                         → সাহায্য দেখাবে
"goodbye jarvis"               → JARVIS বন্ধ করবে
```

---

## ⚙️ কনফিগারেশন

`config/settings.py` ফাইলে সব সেটিংস পরিবর্তন করা যায়:

```python
# ভাষা পরিবর্তন (বাংলায় কথা বলতে)
LANGUAGE = "bn-BD"          # বাংলা
LANGUAGE = "en-US"          # ইংরেজি

# AI মডেল পরিবর্তন
GEMINI_MODEL = "gemini-1.5-pro"   # বেশি শক্তিশালী
GEMINI_MODEL = "gemini-1.5-flash" # দ্রুত (ডিফল্ট)

# ভয়েস গতি পরিবর্তন
TTS_RATE = 150   # ধীর
TTS_RATE = 200   # দ্রুত

# নতুন অ্যাপ যোগ করুন
APPS = {
    "spotify": r"C:\Users\...\Spotify.exe",
    "discord": r"C:\Users\...\Discord.exe",
}
```

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
Voice PC contol/
├── 📄 jarvis.py              ← মূল ফাইল (এটি চালান)
├── 📄 setup.py               ← প্রথমবার সেটআপ
├── 📄 requirements.txt       ← সব লাইব্রেরির তালিকা
├── 📄 README.md              ← এই ফাইল
│
├── ⚙️ config/
│   └── settings.py           ← সব সেটিংস এখানে
│
├── 🧠 core/
│   ├── assistant.py          ← মূল অ্যাসিস্ট্যান্ট ইঞ্জিন
│   ├── ai_brain.py           ← Gemini/OpenAI সংযোগ
│   ├── speech.py             ← ভয়েস ইনপুট/আউটপুট
│   ├── commands.py           ← সিস্টেম কমান্ড প্রসেসর
│   └── display.py            ← টার্মিনাল ডিসপ্লে
│
├── 📋 logs/                  ← লগ ফাইল
├── 🎵 audio/                 ← অডিও ফাইল
└── 💾 data/                  ← ডেটা ফাইল
```

---

## 🔧 সমস্যা সমাধান

### ❌ PyAudio ইনস্টল হচ্ছে না?
```bash
# Windows এ:
pip install pipwin
pipwin install pyaudio
```

### ❌ মাইক্রোফোন কাজ করছে না?
- Windows Settings → Privacy → Microphone → অ্যাপকে অনুমতি দিন

### ❌ Gemini API কাজ করছে না?
- `config/settings.py` তে API Key সঠিকভাবে দেওয়া আছে কিনা চেক করুন
- https://makersuite.google.com এ লগইন করুন

### ❌ ভয়েস শোনা যাচ্ছে না?
- স্পিকার চেক করুন
- `TTS_ENGINE = "gtts"` চেষ্টা করুন settings.py তে

---

## 📜 লাইসেন্স
এই প্রজেক্টটি MIT লাইসেন্সের অধীনে।

---

**তৈরি করেছে Antigravity AI | চালিত Google Gemini দ্বারা** 🚀
