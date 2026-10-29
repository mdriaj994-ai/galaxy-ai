"""
JARVIS Universal Agent - Advanced Automation Engine
এই মডিউলটি ব্যবহারকারীর যেকোনো মুখের কথা (বাংলা বা ইংরেজি) বুঝে কম্পিউটারে যেকোনো কাজ সম্পাদন করে।
"""

import os
import sys
import json
import time
import glob
import datetime
import subprocess
import webbrowser
import urllib.parse
from pathlib import Path

# Safe stdout encoding
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
except ImportError:
    pyautogui = None


class UniversalAgent:
    """কম্পিউটারে যেকোনো কাজ স্বয়ংক্রিয়ভাবে করার কেন্দ্রীয় এআই এজেন্ট।"""

    def __init__(self, settings, ai_brain=None, speech_engine=None):
        self.settings = settings
        self.ai_brain = ai_brain
        self.speech_engine = speech_engine
        self.photoshop_path = self._find_photoshop()
        self.last_speech = ""
        try:
            from core.memory_engine import MemoryEngine
            self.memory = MemoryEngine()
        except Exception as e:
            self.memory = None
            print(f"[!] MemoryEngine load error: {e}", flush=True)

        try:
            from core.commands import CommandProcessor
            self.command_processor = CommandProcessor(settings=self.settings, assistant=self)
        except Exception as e:
            self.command_processor = None
            print(f"[!] CommandProcessor load error: {e}", flush=True)

    def speak(self, text: str):
        """Assistant interface needed by CommandProcessor"""
        self.last_speech = text

    def _find_photoshop(self) -> str:
        common_paths = [
            r"C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop CC 2022\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop CC 2021\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop CC 2020\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop CC 2019\Photoshop.exe",
        ]
        for p in common_paths:
            if os.path.exists(p):
                return p
        # glob দিয়ে যেকোনো version খোঁজো
        try:
            matches = glob.glob(r"C:\Program Files\Adobe\*\Photoshop.exe")
            if matches:
                return matches[0]
        except Exception:
            pass
        # Program Files (x86) চেক
        try:
            matches = glob.glob(r"C:\Program Files (x86)\Adobe\*\Photoshop.exe")
            if matches:
                return matches[0]
        except Exception:
            pass
        return ""

    def _start_process(self, target: str):
        target_lower = target.lower().strip()

        # ── File Explorer ──
        if target_lower in ["explorer", "explorer.exe", "file explorer", "file manager"]:
            try:
                subprocess.Popen(["explorer.exe"])
                return
            except Exception:
                pass
            try:
                os.system("explorer")
                return
            except Exception:
                pass

        # ── Calculator ──
        if target_lower in ["calc", "calc.exe", "calculator"]:
            try:
                subprocess.Popen([r"C:\Windows\System32\calc.exe"])
                return
            except Exception:
                pass
            try:
                subprocess.Popen(["calc.exe"])
                return
            except Exception:
                pass
            try:
                subprocess.Popen("start calc.exe", shell=True)
                return
            except Exception:
                pass

        # ── Antigravity IDE ──
        if target_lower in ["antigravity", "antigravity ide", "agy"]:
            ag_paths = [
                os.path.expandvars(r"%LOCALAPPDATA%\Programs\Antigravity IDE\Antigravity IDE.exe"),
                r"C:\Users\Admin\AppData\Local\Programs\Antigravity IDE\Antigravity IDE.exe",
            ]
            for p in ag_paths:
                if os.path.exists(p):
                    try:
                        os.startfile(p)
                        return
                    except Exception:
                        subprocess.Popen([p])
                        return
            try:
                subprocess.Popen("antigravity", shell=True)
                return
            except Exception:
                pass

        # ── Notepad ──
        if target_lower in ["notepad", "notepad.exe"]:
            try:
                os.startfile("notepad.exe")
                return
            except Exception:
                pass
            try:
                subprocess.Popen("start notepad", shell=True)
                return
            except Exception:
                pass

        # ── Chrome ──
        if target_lower in ["chrome", "chrome.exe", "google chrome"]:
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
            ]
            for p in chrome_paths:
                if os.path.exists(p):
                    try:
                        os.startfile(p)
                        return
                    except Exception:
                        subprocess.Popen([p])
                        return
            try:
                subprocess.Popen("start chrome", shell=True)
                return
            except Exception:
                pass

        # ── Settings ──
        if target_lower in ["settings", "ms-settings:", "উইন্ডোজ সেটিংস"]:
            try:
                subprocess.Popen("start ms-settings:", shell=True)
                return
            except Exception:
                pass

        # ── Task Manager ──
        if target_lower in ["taskmgr", "taskmgr.exe", "task manager"]:
            try:
                os.startfile("taskmgr.exe")
                return
            except Exception:
                pass

        # ── Paint ──
        if target_lower in ["paint", "mspaint", "mspaint.exe"]:
            try:
                os.startfile("mspaint.exe")
                return
            except Exception:
                pass

        # ── CMD ──
        if target_lower in ["cmd", "cmd.exe", "command prompt"]:
            try:
                subprocess.Popen(["cmd.exe"])
                return
            except Exception:
                pass

        # ── Paint ──
        if target_lower in ["paint", "mspaint", "mspaint.exe"]:
            try:
                subprocess.Popen(["mspaint.exe"])
                return
            except Exception:
                pass

        # ── যেকোনো exe বা path ──
        try:
            if os.path.exists(target):
                subprocess.Popen([target])
            else:
                subprocess.Popen(target, shell=True)
            return
        except Exception:
            pass

        try:
            os.startfile(target)
        except Exception:
            pass

    def _open_url(self, url: str):
        # 1. Chrome সরাসরি কল (উইন্ডো অবিলম্বে ফোকাস ও সামনে আনবে)
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        for cp in chrome_paths:
            if os.path.exists(cp):
                try:
                    subprocess.Popen([cp, url])
                    return
                except Exception:
                    pass

        # 2. Windows shell start
        try:
            subprocess.Popen(f'start "" "{url}"', shell=True)
            return
        except Exception:
            pass

        # 3. Windows ShellExecute via os.startfile
        try:
            os.startfile(url)
            return
        except Exception:
            pass

        try:
            webbrowser.open(url)
        except Exception:
            pass

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not text:
            return ""
        import unicodedata
        # Unicode Normalization Form C
        t = unicodedata.normalize('NFC', text)
        # Standardize Bengali character variants
        t = t.replace('\u09af\u09bc', '\u09df')  # yya
        t = t.replace('\u09a1\u09bc', '\u09dc')  # rra
        t = t.replace('\u09a2\u09bc', '\u09dd')  # rha
        # Common phonetic / spelling standardizations
        t = t.replace('সময়', 'সময়')
        t = t.replace('বাড়াও', 'বাড়াও')
        t = t.replace('বাড়া', 'বাড়া')
        t = t.replace('কমাও', 'কমাও')
        t = t.replace('কী বার', 'কি বার')
        t = t.replace('খুলো', 'খোলো')
        return t.strip().lower()

    def execute(self, user_command: str) -> dict:
        """
        ব্যবহারকারীর বাংলা বা ইংরেজি কমান্ড বিশ্লেষণ করে উপযুক্ত কাজ সম্পন্ন করে।
        """
        if not user_command or not user_command.strip():
            return {
                "success": False,
                "action": "none",
                "reply": "আমি কিছু শুনতে পাইনি। অনুগ্রহ করে আবার বলুন।",
                "details": "Empty input"
            }

        cmd_clean = user_command.strip()
        cmd_lower = self._normalize_text(cmd_clean)

        print(f"[*] Processing command: {cmd_clean} (normalized: {cmd_lower})", flush=True)

        # 0. স্মৃতি ও দৈনিক কাজের ট্র্যাকিং (আজকের কাজ, কাজ শেষ, কাজের হিসাব, মনে রাখো)
        mem_res = self._handle_memory_and_tasks(cmd_clean, cmd_lower)
        if mem_res:
            if hasattr(self, 'memory') and self.memory:
                self.memory.log_chat("user", cmd_clean)
                self.memory.log_chat("assistant", mem_res.get("reply", ""))
            return mem_res

        # 1. দ্রুত বাংলা/ইংরেজি প্যাটার্ন ম্যাচিং
        quick = self._quick_match(cmd_clean, cmd_lower)
        if quick:
            return quick

        # 2. সাধারণ অ্যাপ
        app = self._handle_common_apps(cmd_lower)
        if app:
            return app

        # 3. Full PC Command Processor (মাউস, কীবোর্ড, উইন্ডো, সাউন্ড, সিস্টেম)
        if self.command_processor:
            self.last_speech = ""
            handled = self.command_processor.process(cmd_clean) or self.command_processor.process(cmd_lower)
            if handled:
                reply = self.last_speech or "কাজটি সম্পন্ন হয়েছে।"
                return {
                    "success": True,
                    "action": "system_command",
                    "reply": reply,
                    "details": f"Executed: {cmd_clean}"
                }

        # 4. Gemini AI দিয়ে গভীর বিশ্লেষণ
        return self._ai_directed_execution(cmd_clean)

    # ══════════════════════════════════════════════════
    # ⚡ QUICK MATCH — বাংলা + ইংরেজি সব কমান্ড
    # ══════════════════════════════════════════════════
    def _quick_match(self, raw: str, low: str) -> dict:

        # ────── ইউটিউব ──────
        yt_bn = ["ইউটিউব", "ইউটিউবে", "ইউটিউব এ", "গান বাজাও", "গান চালাও", "মিউজিক চালাও"]
        yt_en = ["youtube", "yt", "play song", "play music", "play video"]
        is_yt = any(w in low for w in yt_bn) or any(w == low or low.startswith(w + " ") or f" {w} " in f" {low} " for w in yt_en)
        if is_yt:
            # যদি শুধুই ওপেন করার অনুরোধ হয়
            pure_open = ["খোলো", "খুলো", "খোল", "ওপেন করো", "ওপেন কর", "চালু করো", "চালু কর", "দেখাও", "যাও", "ঢোকো", "ঢোক", "open", "launch", "kholo", "chalu koro"]
            is_just_open = any(op in low for op in pure_open) and not any(w in low for w in ["সার্চ", "গান", "বাজাও", "চালাও", "search", "play"])
            if is_just_open or low in ["youtube", "yt", "ইউটিউব"]:
                url = "https://www.youtube.com"
                self._open_url(url)
                return {"success": True, "action": "open_website",
                        "reply": "ইউটিউব খোলা হচ্ছে।",
                        "url": url,
                        "details": "Opened YouTube"}

            query = raw
            stops = [
                "ইউটিউব এ গিয়ে", "ইউটিউবে গিয়ে", "ইউটিউবে গিয়া", "ইউটিউব এ গিয়া",
                "ইউটিউবে", "ইউটিউব এ", "ইউটিউব", "youtube", "yt",
                "গিয়ে", "গিয়া", "সার্চ করো", "সার্চ কর", "সার্চ করুন",
                "খোলো", "খুলো", "খোল", "ওপেন করো", "ওপেন কর", "চালু করো", "চালু কর",
                "open", "launch", "kholo",
                "বাজাও", "চালাও", "চালাও দেও",
                "search", "play", "video"
            ]
            for s in stops:
                query = query.replace(s, "")
            query = query.strip()
            if not query:
                url = "https://www.youtube.com"
                self._open_url(url)
                return {"success": True, "action": "open_website",
                        "reply": "ইউটিউব খোলা হচ্ছে।",
                        "url": url,
                        "details": "Opened YouTube"}

            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
            self._open_url(url)
            return {"success": True, "action": "youtube",
                    "reply": f"ইউটিউবে \"{query}\" সার্চ করা হচ্ছে।",
                    "url": url,
                    "details": f"YouTube: {query}"}


        # ────── গুগল সার্চ ──────
        g_bn = ["গুগল", "গুগলে", "সার্চ করো", "সার্চ কর", "সার্চ করুন", "খুঁজে দাও", "খুঁজে দে"]
        g_en = ["google", "search for", "search", "find"]
        if any(w in low for w in g_bn + g_en):
            query = raw
            stops = ["গুগলে গিয়ে", "গুগলে", "গুগল", "google", "সার্চ করো", "সার্চ কর",
                     "সার্চ করুন", "খুঁজে দাও", "খুঁজে দে", "search for", "search", "find"]
            for s in stops:
                query = query.replace(s, "")
            query = query.strip()
            if query:
                url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
                self._open_url(url)
                return {"success": True, "action": "web_search",
                        "reply": f"গুগলে \"{query}\" সার্চ করা হচ্ছে।",
                        "url": url,
                        "details": f"Google: {query}"}

        # ────── সময় ──────
        t_bn = ["সময় কত", "কয়টা বাজে", "কয়টা বাজল", "এখন কটা", "সময় বলো", "টাইম বলো"]
        t_en = ["what time", "current time", "time is it", "tell me the time"]
        if any(w in low for w in t_bn + t_en):
            now = datetime.datetime.now().strftime("%I:%M %p")
            return {"success": True, "action": "time",
                    "reply": f"এখন সময় হলো {now}",
                    "details": f"Time: {now}"}

        # ────── দিন / বার ──────
        day_bn = ["কি বার", "কী বার", "কোন দিন", "আজকের দিন", "আজ কি বার", "আজকে কি বার"]
        day_en = ["what day", "day of the week", "which day is today"]
        if any(w in low for w in day_bn + day_en):
            days_map = {
                0: "সোমবার",
                1: "মঙ্গলবার",
                2: "বুধবার",
                3: "বৃহস্পতিবার",
                4: "শুক্রবার",
                5: "শনিবার",
                6: "রবিবার"
            }
            weekday = days_map.get(datetime.datetime.now().weekday(), "")
            date_str = datetime.datetime.now().strftime("%d %B %Y")
            return {"success": True, "action": "day",
                    "reply": f"আজ {weekday}, {date_str}।",
                    "details": f"Day: {weekday}"}

        # ────── তারিখ ──────
        d_bn = ["আজকে কত তারিখ", "আজ কত তারিখ", "তারিখ কত", "আজকের তারিখ", "তারিখ বলো"]
        d_en = ["what date", "today's date", "current date"]
        if any(w in low for w in d_bn + d_en):
            now = datetime.datetime.now().strftime("%d %B %Y")
            return {"success": True, "action": "date",
                    "reply": f"আজকের তারিখ হলো {now}",
                    "details": f"Date: {now}"}

        # ────── ব্যাটারি / চার্জ ──────
        bat_bn = ["ব্যাটারি কত", "ব্যাটারি চার্জ", "চার্জ কত", "ব্যাটারির অবস্থা", "চার্জ কতটুকু", "ব্যাটারি লেভেল"]
        bat_en = ["battery", "battery level", "battery percentage"]
        if any(w in low for w in bat_bn + bat_en):
            try:
                import psutil
                b = psutil.sensors_battery()
                if b is not None:
                    status = "চার্জ হচ্ছে" if b.power_plugged else "ব্যাটারিতে চলছে"
                    return {"success": True, "action": "battery",
                            "reply": f"ব্যাটারি চার্জ আছে {int(b.percent)} শতাংশ এবং {status}।",
                            "details": f"Battery: {b.percent}%"}
                else:
                    return {"success": True, "action": "battery",
                            "reply": "আপনার কম্পিউটার সরাসরি বিদ্যুৎ লাইনে চলছে (ডেস্কটপ পিসি)।",
                            "details": "Desktop AC power"}
            except Exception:
                return {"success": True, "action": "battery",
                        "reply": "কম্পিউটার পাওয়ার সাপ্লাই সংযুক্ত আছে।",
                        "details": "AC Power"}

        # ────── কুশল বিনিময় / পরিচয় ──────
        greet_bn = ["কেমন আছো", "কেমন আছেন", "কি খবর", "ভালো আছো", "কেমন চলতাছে"]
        greet_en = ["how are you", "how are you doing", "what's up"]
        if any(w in low for w in greet_bn + greet_en):
            return {"success": True, "action": "greeting",
                    "reply": "আমি খুব ভালো আছি! আপনার জন্য কী কাজ করতে পারি বলুন?",
                    "details": "Greeting"}

        who_bn = ["তুমি কে", "তোমার নাম কি", "কে তুমি", "তোমার পরিচয়", "জারভিস কে"]
        who_en = ["who are you", "what is your name", "who made you"]
        if any(w in low for w in who_bn + who_en):
            return {"success": True, "action": "identity",
                    "reply": "আমি জারভিস, আপনার ব্যক্তিগত এআই ভয়েস এবং পিসি কন্ট্রোল অ্যাসিস্ট্যান্ট।",
                    "details": "Identity"}

        hi_bn = ["হ্যালো", "হাই", "শুনছো", "শুনছিস", "আছো নাকি"]
        hi_en = ["hello", "hi", "hey jarvis"]
        if any(low == w or low.startswith(w + " ") for w in hi_bn + hi_en):
            return {"success": True, "action": "hello",
                    "reply": "হ্যাঁ, আমি শুনছি! বলুন কী করতে হবে।",
                    "details": "Hello"}

        # ────── রিসাইকেল বিন খালি করো ──────
        rb_bn = ["রিসাইকেল বিন খালি", "ট্র্যাশ খালি", "রিসাইকেল বিন পরিষ্কার"]
        rb_en = ["empty recycle bin", "empty trash", "clear recycle bin"]
        if any(w in low for w in rb_bn + rb_en):
            subprocess.run(["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"], capture_output=True)
            return {"success": True, "action": "empty_recycle_bin",
                    "reply": "রিসাইকেল বিন সম্পূর্ণ খালি করা হয়েছে।", "details": "Recycle Bin cleared"}

        # ────── সব মিনিমাইজ করো / ডেস্কটপ দেখাও ──────
        min_bn = ["মিনিমাইজ করো", "সব মিনিমাইজ", "মিনিমাইজ", "ডেস্কটপে যাও"]
        min_en = ["minimize all", "minimize", "show desktop"]
        if any(w in low for w in min_bn + min_en):
            subprocess.run(["powershell", "-Command", "(New-Object -ComObject Shell.Application).MinimizeAll()"], capture_output=True)
            return {"success": True, "action": "minimize_all",
                    "reply": "সব উইন্ডো মিনিমাইজ করা হয়েছে।", "details": "Minimized all windows"}

        # ────── সেটিংস খোলো ──────
        set_bn = ["সেটিংস খোলো", "উইন্ডোজ সেটিংস", "সেটিংস চালু করো"]
        set_en = ["open settings", "windows settings", "settings"]
        if any(w in low for w in set_bn + set_en):
            subprocess.Popen("start ms-settings:", shell=True)
            return {"success": True, "action": "open_settings",
                    "reply": "উইন্ডোজ সেটিংস খোলা হচ্ছে।", "details": "Opened Settings"}

        # ────── টাস্ক ম্যানেজার ──────
        tm_bn = ["টাস্ক ম্যানেজার", "টাস্ক ম্যানেজার খোলো"]
        tm_en = ["task manager", "open task manager"]
        if any(w in low for w in tm_bn + tm_en):
            subprocess.Popen("taskmgr.exe", shell=True)
            return {"success": True, "action": "open_app",
                    "reply": "টাস্ক ম্যানেজার চালু হচ্ছে।", "details": "Opened Task Manager"}

        # ────── ভলিউম বাড়াও ──────
        vup_bn = ["ভলিউম বাড়াও", "ভলিউম বাড়া", "আওয়াজ বাড়াও", "শব্দ বাড়াও", "লাউড করো"]
        vup_en = ["volume up", "increase volume", "louder", "turn up"]
        if any(w in low for w in vup_bn + vup_en):
            try:
                self._volume_change("up")
            except Exception:
                pass
            return {"success": True, "action": "volume_up",
                    "reply": "ভলিউম বাড়ানো হয়েছে।", "details": "Volume increased"}

        # ────── ভলিউম কমাও ──────
        vdn_bn = ["ভলিউম কমাও", "ভলিউম কমা", "আওয়াজ কমাও", "শব্দ কমাও", "নিচু করো"]
        vdn_en = ["volume down", "decrease volume", "quieter", "lower volume", "turn down"]
        if any(w in low for w in vdn_bn + vdn_en):
            try:
                self._volume_change("down")
            except Exception:
                pass
            return {"success": True, "action": "volume_down",
                    "reply": "ভলিউম কমানো হয়েছে।", "details": "Volume decreased"}

        # ────── মিউট ──────
        mute_bn = ["মিউট করো", "মিউট কর", "আওয়াজ বন্ধ করো", "শব্দ বন্ধ করো", "সাইলেন্ট করো"]
        mute_en = ["mute", "silence", "quiet"]
        if any(w in low for w in mute_bn + mute_en):
            try:
                self._mute()
            except Exception:
                pass
            return {"success": True, "action": "mute",
                    "reply": "সাউন্ড মিউট করা হয়েছে।", "details": "Muted"}

        # ────── স্ক্রিনশট ──────
        ss_bn = ["স্ক্রিনশট নাও", "স্ক্রিনশট নে", "স্ক্রিন ক্যাপচার", "স্ক্রিনশট করো"]
        ss_en = ["screenshot", "take screenshot", "capture screen", "screen capture"]
        if any(w in low for w in ss_bn + ss_en):
            result = self._take_screenshot()
            return {"success": True, "action": "screenshot",
                    "reply": result, "details": "Screenshot taken"}

        # ────── স্ক্রিন লক ──────
        lock_bn = ["স্ক্রিন লক করো", "কম্পিউটার লক করো", "পিসি লক করো", "লক করো"]
        lock_en = ["lock screen", "lock computer", "lock pc", "lock workstation"]
        if any(w in low for w in lock_bn + lock_en):
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            return {"success": True, "action": "lock",
                    "reply": "স্ক্রিন লক করা হয়েছে।", "details": "Screen locked"}

        # ────── শাটডাউন ──────
        sd_bn = ["কম্পিউটার বন্ধ করো", "পিসি বন্ধ করো", "শাটডাউন দাও", "বন্ধ করে দাও"]
        sd_en = ["shutdown", "shut down", "power off"]
        if any(w in low for w in sd_bn + sd_en):
            subprocess.Popen("shutdown /s /t 10", shell=True)
            return {"success": True, "action": "shutdown",
                    "reply": "কম্পিউটার ১০ সেকেন্ড পরে বন্ধ হবে।", "details": "Shutdown in 10s"}

        # ────── রিস্টার্ট ──────
        rs_bn = ["কম্পিউটার রিস্টার্ট করো", "রিস্টার্ট দাও", "পুনরায় চালু করো"]
        rs_en = ["restart", "reboot"]
        if any(w in low for w in rs_bn + rs_en):
            subprocess.Popen("shutdown /r /t 10", shell=True)
            return {"success": True, "action": "restart",
                    "reply": "কম্পিউটার ১০ সেকেন্ড পরে রিস্টার্ট হবে।", "details": "Restart in 10s"}

        # ────── ফটোশপ ──────
        ps_bn = ["ফটোশপ", "ফটশপ", "ফটোসপ", "ফোটোশপ"]
        ps_en = ["photoshop"]
        if any(w in low for w in ps_bn + ps_en):
            return self._handle_photoshop(raw)

        # ────── হোয়াটসঅ্যাপে ফোল্ডারের ছবি/ফাইল অটো সেন্ড ──────
        is_wa = any(w in low for w in ["whatsapp", "হোয়াটসঅ্যাপ", "হোয়াটসঅ্যাপ", "ওয়াটসঅ্যাপ"])
        is_send_intent = any(w in low for w in ["send", "pathao", "পাঠাও", "dao", "দাও", "sed", "দিবে", "দিয়ে", "ফরওয়ার্ড"])
        is_folder_intent = any(w in low for w in ["drive", "ড্রাইভ", "folder", "ফোল্ডার", "file", "ফাইল", "photo", "ছবি", "image", "all photo"])
        if is_wa and (is_send_intent or is_folder_intent):
            res = self._handle_folder_to_whatsapp(raw, low)
            if res:
                return res

        # ────── Facebook Auto-Login ──────
        fb_login_bn = ["ফেসবুকে লগইন", "ফেসবুক লগইন", "ফেসবুকে ঢোকো", "ফেসবুক ঢোকো",
                       "ফেসবুকে লগ ইন", "ফেসবুক এ ঢোকো", "ফেসবুকে সাইন ইন"]
        fb_login_en = ["login to facebook", "log into facebook", "sign in facebook",
                       "facebook login", "facebook sign in", "open facebook and login"]
        if any(w in low for w in fb_login_bn + fb_login_en):
            return self._facebook_login_start(raw)

        # ────── ওয়েবসাইট খোলো ──────
        web_map = {
            "ফেসবুক": "https://facebook.com",
            "facebook": "https://facebook.com",
            "fb": "https://facebook.com",
            "ইনস্টাগ্রাম": "https://instagram.com",
            "instagram": "https://instagram.com",
            "টুইটার": "https://twitter.com",
            "twitter": "https://twitter.com",
            "জিমেইল": "https://mail.google.com",
            "gmail": "https://mail.google.com",
            "হোয়াটসঅ্যাপ": "https://web.whatsapp.com",
            "হোয়াটসঅ্যাপ": "https://web.whatsapp.com",
            "whatsapp": "https://web.whatsapp.com",
            "গিটহাব": "https://github.com",
            "github": "https://github.com",
            "নেটফ্লিক্স": "https://netflix.com",
            "netflix": "https://netflix.com",
            "উইকিপিডিয়া": "https://wikipedia.org",
            "wikipedia": "https://wikipedia.org",
            "চ্যাটজিপিটি": "https://chat.openai.com",
            "chatgpt": "https://chat.openai.com",
        }
        open_bn = ["খোলো", "খুলো", "খোল", "ওপেন করো", "ওপেন কর", "চালু করো", "চালু কর", "দেখাও", "যাও", "ঢোকো", "ঢোক"]
        open_en = ["open", "go to", "launch", "show", "kholo", "chalu koro", "visit"]
        is_question = any(q in low for q in ["কে", "কি", "কী", "কবে", "কত", "কেন", "কার", "কোথায়", "who", "when", "how", "what", "why"])
        for site_key, site_url in web_map.items():
            if site_key in low:
                # যদি কোনো প্রশ্ন করা হয় (যেমন: ফেসবুক কে তৈরি করেছে), তাহলে ওয়েবসাইট ওপেন না করে উত্তর দাও
                if is_question and not any(op in low for op in open_bn + open_en):
                    continue
                self._open_url(site_url)
                return {"success": True, "action": "open_website",
                        "reply": f"{site_key} খোলা হচ্ছে।",
                        "url": site_url,
                        "details": f"Opened {site_url}"}

        # ────── ক্যালকুলেটর ──────
        calc_bn = ["ক্যালকুলেটর", "ক্যালকুলেটর চালু করো", "হিসাব করতে হবে"]
        calc_en = ["calculator", "calc"]
        if any(w in low for w in calc_bn + calc_en):
            self._start_process("calc")
            return {"success": True, "action": "open_app",
                    "reply": "ক্যালকুলেটর চালু হচ্ছে।", "details": "Opened Calculator"}

        # ────── Antigravity IDE ──────
        ag_bn = ["অ্যান্টিগ্র্যাভিটি", "অ্যান্টি গ্র্যাভিটি", "এন্টিগ্র্যাভিটি", "এন্টি গ্রাভিটি", "এন্ট্রি গ্রাভিটি", "এন্ট্রি কাবাডি"]
        ag_en = ["antigravity", "antigravity ide", "agy"]
        if any(w in low for w in ag_bn + ag_en):
            if any(w in low for w in ["চ্যাট", "লেখ", "পাঠাও", "টাইপ", "মেসেজ", "chat"]):
                return self._handle_antigravity_action(raw, low)
            self._start_process("antigravity")
            return {"success": True, "action": "open_app",
                    "reply": "অ্যান্টিগ্র্যাভিটি আইডিই চালু হচ্ছে।", "details": "Opened Antigravity IDE"}

        # ────── নোটপ্যাড ──────
        np_bn = ["নোটপ্যাড", "নোট প্যাড", "নোটপ্যাড খোলো"]
        np_en = ["notepad"]
        if any(w in low for w in np_bn + np_en):
            self._start_process("notepad")
            return {"success": True, "action": "open_app",
                    "reply": "নোটপ্যাড চালু হচ্ছে।", "details": "Opened Notepad"}

        # ────── ডিস্ক স্পেস / ড্রাইভের ফাঁকা জায়গা চেক ──────
        is_space_query = any(w in low for w in ["ফাঁকা", "স্পেস", "space", "size", "সাইজ", "কত জিবি", "কতটুকু", "পার্সেন্ট", "শতাংশ", "ফ্রি", "free"])
        is_drive_mention = any(w in low for w in ["ড্রাইভ", "drive", "সি ড্রাইভ", "c drive", "ডি ড্রাইভ", "d drive", "ডিস্ক", "মেমোরি"])
        if is_space_query or (is_drive_mention and any(w in low for w in ["কত", "দেখো", "বলো", "চেক"])):
            try:
                import shutil
                drive = "C:\\"
                drive_name = "সি"
                if "ডি ড্রাইভ" in low or "d drive" in low or " d:" in low or "d ড্রাইভ" in low:
                    drive = "D:\\"
                    drive_name = "ডি"
                elif "ই ড্রাইভ" in low or "e drive" in low or " e:" in low or "e ড্রাইভ" in low:
                    drive = "E:\\"
                    drive_name = "ই"

                total, used, free = shutil.disk_usage(drive)
                total_gb = round(total / (1024**3), 1)
                free_gb = round(free / (1024**3), 1)
                used_gb = round(used / (1024**3), 1)
                percent_free = round((free / total) * 100, 1)

                try:
                    subprocess.Popen(["explorer.exe", drive])
                except Exception:
                    pass

                reply = f"আপনার কম্পিউটারের {drive_name} ড্রাইভ খোলা হয়েছে। মোট {total_gb} জিবির মধ্যে {free_gb} জিবি অর্থাৎ প্রায় {percent_free} শতাংশ ফাঁকা আছে।"
                return {"success": True, "action": "disk_space",
                        "reply": reply,
                        "details": f"{drive} Free: {free_gb}GB / {total_gb}GB ({percent_free}%)"}
            except Exception:
                pass

        # ────── ফাইল এক্সপ্লোরার ──────
        fe_bn = ["ফাইল এক্সপ্লোরার", "মাই কম্পিউটার", "ফাইল ম্যানেজার", "এক্সপ্লোরার", "দিস পিসি", "দিসপিসি", "কম্পিউটার খোলো", "ফাইল খোলো", "ফাইল দেখাও", "ফোল্ডার খোলো"]
        fe_en = ["file explorer", "my computer", "explorer", "file manager", "this pc", "open files"]
        if any(w in low for w in fe_bn + fe_en):
            self._start_process("explorer")
            return {"success": True, "action": "open_app",
                    "reply": "ফাইল এক্সপ্লোরার চালু হচ্ছে।", "details": "Opened File Explorer"}

        # ────── ক্রোম ব্রাউজার ──────
        ch_bn = ["ক্রোম", "ব্রাউজার খোলো", "ক্রোম খোলো", "ইন্টারনেট খোলো"]
        ch_en = ["chrome", "open browser", "open chrome"]
        if any(w in low for w in ch_bn + ch_en):
            self._start_process("chrome")
            return {"success": True, "action": "open_app",
                    "reply": "গুগল ক্রোম চালু হচ্ছে।", "details": "Opened Chrome"}

        # ────── ডাউনলোড ফোল্ডার ──────
        dl_bn = ["ডাউনলোড ফোল্ডার", "ডাউনলোড খোলো", "ডাউনলোড দেখাও"]
        dl_en = ["downloads folder", "open downloads", "show downloads"]
        if any(w in low for w in dl_bn + dl_en):
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            self._start_process(path)
            return {"success": True, "action": "open_folder",
                    "reply": "ডাউনলোড ফোল্ডার খোলা হচ্ছে।", "details": f"Opened {path}"}

        # ────── ডেস্কটপ দেখাও ──────
        desk_bn = ["ডেস্কটপ দেখাও", "ডেস্কটপ খোলো", "ডেস্কটপ ফোল্ডার"]
        desk_en = ["show desktop", "open desktop"]
        if any(w in low for w in desk_bn + desk_en):
            path = os.path.join(os.path.expanduser("~"), "Desktop")
            self._start_process(path)
            return {"success": True, "action": "open_folder",
                    "reply": "ডেস্কটপ ফোল্ডার খোলা হচ্ছে।", "details": f"Opened Desktop"}

        # ────── কমান্ড প্রম্পট ──────
        cmd_bn = ["কমান্ড প্রম্পট", "টার্মিনাল খোলো", "cmd খোলো"]
        cmd_en = ["command prompt", "terminal", "cmd"]
        if any(w in low for w in cmd_bn + cmd_en):
            self._start_process("cmd")
            return {"success": True, "action": "open_app",
                    "reply": "কমান্ড প্রম্পট চালু হচ্ছে।", "details": "Opened CMD"}

        # ────── ড্রাইভ ওপেনার (D Drive, C Drive, etc.) ──────
        drive_patterns = [
            ("d drive", "D:\\", "ডি ড্রাইভ"),
            ("d:", "D:\\", "ডি ড্রাইভ"),
            ("ডি ড্রাইভ", "D:\\", "ডি ড্রাইভ"),
            ("c drive", "C:\\", "সি ড্রাইভ"),
            ("c:", "C:\\", "সি ড্রাইভ"),
            ("সি ড্রাইভ", "C:\\", "সি ড্রাইভ"),
            ("e drive", "E:\\", "ই ড্রাইভ"),
            ("e:", "E:\\", "ই ড্রাইভ"),
        ]
        # শুধু ড্রাইভ ওপেন করার ইচ্ছা থাকলে
        if any(dp[0] in low for dp in drive_patterns) and not any(w in low for w in ["whatsapp", "হোয়াটসঅ্যাপ", "হোয়াটসঅ্যাপ"]):
            if any(v in low for v in ["খোল", "open", "jao", "যাও", "dhoko", "ঢোক", "dekhao", "দেখাও", "show"]):
                for key, path, name_bn in drive_patterns:
                    if key in low:
                        self._start_process(path)
                        return {"success": True, "action": "open_drive",
                                "reply": f"{name_bn} খোলা হচ্ছে।", "details": f"Opened {path}"}

        # ────── Direct Login / Submit Click ──────
        login_bn = ["লগইন করো", "লগ ইন করো", "লগইন এ ক্লিক করো", "লগইন বাটন", "সাইন ইন করো", "enter চাপো", "এন্টার চাপো", "লগইন"]
        login_en = ["login now", "click login", "press enter", "submit login", "log in", "login"]
        if any(w in low for w in login_bn + login_en):
            try:
                if pyautogui:
                    pyautogui.press('enter')
                    return {"success": True, "action": "press_enter",
                            "reply": "লগইন বাটনে ক্লিক করে লগইন করা হচ্ছে।", "details": "Pressed Enter for login"}
            except Exception:
                pass

        # ────── Login number/phone input ──────
        phone_bn = ["আমার নম্বর", "নম্বর হলো", "নাম্বার হলো", "মোবাইল নম্বর",
                    "ফোন নম্বর", "আমার ইমেইল", "ইউজার নেম", "নাম্বার", "নম্বর"]
        phone_en = ["my number is", "number is", "phone number", "email is", "username is", "number", "email"]
        if any(w in low for w in phone_bn + phone_en):
            import re
            numbers = re.findall(r'[\d\+\-\s]{7,}', raw)
            email_match = re.findall(r'[\w\.\-]+@[\w\.\-]+\.\w+', raw)
            val = email_match[0] if email_match else (''.join(numbers[0].split()) if numbers else raw)
            for kw in phone_bn + phone_en:
                if kw in low:
                    val = raw[raw.lower().find(kw) + len(kw):].strip().strip(":=- ")
                    break
            return self._type_in_active_field(val, "phone/email")

        # ────── Password input ──────
        pass_bn = ["পাসওয়ার্ড হলো", "পাসওয়ার্ড হচ্ছে", "পাসওয়ার্ড দাও", "পাসওয়ার্ড টাইপ করো", "পাসওয়ার্ড"]
        pass_en = ["password is", "my password", "type password", "password"]
        if any(w in low for w in pass_bn + pass_en):
            import re
            for kw in ["পাসওয়ার্ড হলো", "পাসওয়ার্ড হচ্ছে", "পাসওয়ার্ড দাও", "পাসওয়ার্ড", "password is", "my password is", "password"]:
                if kw in low:
                    pwd = raw[raw.lower().find(kw) + len(kw):].strip().strip(":=- ")
                    if pwd:
                        return self._type_password_and_login(pwd)
            return self._type_password_and_login(raw)

        # ────── গাণিতিক হিসাব ও ক্যালকুলেটরে লাইভ টাইপিং ──────
        calc_triggers = ["হিসাব করো", "হিসাব", "calculate", "কত হয়", "কত হয়", "যোগ করো", "গুণ করো", "বিয়োগ করো", "ভাগ করো", "গুন করো"]
        if any(w in low for w in calc_triggers) or (any(op in low for op in ["গুণ", "গুন", "প্লাস", "মাইনাস", "ডিভাইডেড"]) and any(c.isdigit() for c in raw)):
            res = self._calculate_and_type_math(raw, low)
            if res and res.get("success"):
                return res

        # ────── Antigravity IDE ও চ্যাট বক্স অটোমেশন ──────
        ag_triggers = ["এন্ট্রি গ্রাভিটি", "এন্টিগ্র্যাভিটি", "অ্যান্টিগ্র্যাভিটি", "অ্যান্টি গ্র্যাভিটি", "এন্ট্রি কাবাডি", "antigravity", "agy"]
        if any(w in low for w in ag_triggers) or any(w in low for w in ["চ্যাট বক্সে লেখ", "চ্যাটে লেখ", "চ্যাটবক্সে লেখ", "এন্টিগ্র্যাভিটিতে লেখ"]):
            return self._handle_antigravity_action(raw, low)

        return None

    # ══════════════════════════════════════════════════
    # 🖥️ Common Apps
    # ══════════════════════════════════════════════════
    def _handle_common_apps(self, low: str) -> dict:
        apps = {
            "notepad": (["নোটপ্যাড", "নোট প্যাড", "notepad"], "notepad", "নোটপ্যাড"),
            "calc":    (["ক্যালকুলেটর", "calculator", "calc"], "calc", "ক্যালকুলেটর"),
            "chrome":  (["ক্রোম", "chrome", "গুগল ক্রোম", "ব্রাউজার"], "chrome", "গুগল ক্রোম"),
            "explorer":(["ফাইল এক্সপ্লোরার", "মাই কম্পিউটার", "দিস পিসি", "ফাইল ম্যানেজার", "explorer"], "explorer", "ফাইল এক্সপ্লোরার"),
            "cmd":     (["কমান্ড প্রম্পট", "টার্মিনাল", "cmd"], "cmd", "কমান্ড প্রম্পট"),
            "paint":   (["পেইন্ট", "paint", "mspaint"], "paint", "পেইন্ট"),
            "settings":(["সেটিংস", "উইন্ডোজ সেটিংস", "settings"], "settings", "উইন্ডোজ সেটিংস"),
            "taskmgr": (["টাস্ক ম্যানেজার", "টাস্কম্যানেজার", "task manager", "taskmgr"], "taskmgr", "টাস্ক ম্যানেজার"),
        }
        for app_id, (triggers, exe_target, name_bn) in apps.items():
            if any(t in low for t in triggers):
                if any(w in low for w in ["বন্ধ করো", "close", "kill", "বন্ধ কর"]):
                    os.system(f"taskkill /f /im {exe_target}.exe >nul 2>&1")
                    return {"success": True, "action": "close_app",
                            "reply": f"{name_bn} বন্ধ করা হয়েছে।", "details": f"Closed {exe_target}"}
                else:
                    self._start_process(exe_target)
                    return {"success": True, "action": "open_app",
                            "reply": f"{name_bn} চালু করা হচ্ছে।", "details": f"Opened {name_bn}"}
        return None

    # ══════════════════════════════════════════════════
    # 🔊 ভলিউম কন্ট্রোল (Windows Native ctypes keybd_event)
    # ══════════════════════════════════════════════════
    def _volume_change(self, direction: str):
        try:
            import ctypes
            key_code = 0xAF if direction == "up" else 0xAE
            for _ in range(5):
                ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
                ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)
        except Exception as e:
            print(f"[Volume Error]: {e}", flush=True)

    def _mute(self):
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
        except Exception as e:
            print(f"[Mute Error]: {e}", flush=True)

    # ══════════════════════════════════════════════════
    # 📸 Screenshot
    # ══════════════════════════════════════════════════
    def _take_screenshot(self) -> str:
        try:
            self._start_process("snippingtool")
            return "স্ক্রিনশট টুল চালু হয়েছে, স্ক্রিনশট নিন।"
        except Exception as e:
            return f"স্ক্রিনশট টুল চালু করতে সমস্যা: {e}"

    # ══════════════════════════════════════════════════
    # 🎨 Photoshop
    # ══════════════════════════════════════════════════
    def _handle_photoshop(self, raw: str) -> dict:
        path = self.photoshop_path
        # যদি path খালি বা exe না থাকে, আবার খোঁজো
        if not path or not os.path.exists(path):
            path = self._find_photoshop()
            self.photoshop_path = path

        if path and os.path.exists(path):
            try:
                subprocess.Popen([path])
                return {"success": True, "action": "photoshop",
                        "reply": "ফটোশপ চালু করা হচ্ছে।",
                        "details": f"Launched: {path}"}
            except Exception as e:
                return {"success": False, "action": "photoshop",
                        "reply": f"ফটোশপ খুলতে সমস্যা হলো: {e}", "details": str(e)}
        else:
            return {"success": False, "action": "photoshop",
                    "reply": "ফটোশপ ইনস্টল করা নেই অথবা খুঁজে পাওয়া যাচ্ছে না।",
                    "details": "Photoshop not found"}

    # ══════════════════════════════════════════════════
    # 📁 Antigravity
    # ══════════════════════════════════════════════════
    def _handle_antigravity_files(self) -> dict:
        try:
            workspace = Path(__file__).parent.parent
            py_files = list(workspace.glob("**/*.py"))
            return {"success": True, "action": "antigravity_check",
                    "reply": f"প্রজেক্টে মোট {len(py_files)}টি পাইথন ফাইল সক্রিয় আছে।",
                    "details": f"{len(py_files)} Python files found"}
        except Exception as e:
            return {"success": False, "action": "antigravity_check",
                    "reply": f"ফাইল চেক করতে সমস্যা: {e}", "details": str(e)}

    def _handle_antigravity_account(self) -> dict:
        url = "https://aistudio.google.com/app/apikey"
        self._open_url(url)
        return {"success": True, "action": "antigravity_account",
                "reply": "Google AI Studio লগইন পেজ খোলা হয়েছে।",
                "details": f"Opened {url}"}

    # ══════════════════════════════════════════════════
    # ══════════════════════════════════════════════════
    # 🧠 Memory & Daily Tasks Handler
    # ══════════════════════════════════════════════════
    def _handle_memory_and_tasks(self, raw: str, low: str) -> dict | None:
        """স্মৃতি সংরক্ষণ, সারাদিনের কাজের তালিকা রাখা ও ট্র্যাকিং পরিচালনা করে।"""
        if not hasattr(self, 'memory') or not self.memory:
            return None

        # ────── ১. সারাদিনের কাজের তালিকা যোগ করা ──────
        is_add_task = any(p in low for p in [
            "সারাদিনের কাজ", "আজকের কাজ", "আজকে আমার কাজ", "আজকের টুডু",
            "কাজের লিস্ট", "আজকে যা যা করব", "আজকে যা করব", "আজকের টাস্ক",
            "daily tasks", "tasks for today"
        ]) and not any(p in low for p in ["কি কি", "কী কী", "হিসাব", "বলো", "শেষ", "করছি", "করসি", "করেছি", "done"])

        if is_add_task:
            tasks = []
            # Fast pattern extraction if numbers or bullets exist (Instant 0.001s)
            import re
            if re.search(r'[১-৯1-9][\.\)\-\s]', raw):
                parts = re.split(r'[১-৯1-9][\.\)\-\s]', raw)
                tasks = [p.strip(" \t\n\r,.-") for p in parts if len(p.strip(" \t\n\r,.-")) > 2]
                tasks = [t for t in tasks if not any(w in t.lower() for w in ["সারাদিনের", "আজকের কাজ", "লিস্ট", "কাজ হলো", "কাজ হল"])]

            # AI fallback if no numbers present
            if not tasks and self.ai_brain:
                prompt = f"""Extract the individual task items from this Bengali/English sentence as a JSON array of strings:
Sentence: "{raw}"
Example output format: ["task 1", "task 2", "task 3"]
Output ONLY the JSON array:"""
                try:
                    res = self.ai_brain.get_response(prompt)
                    clean = res.strip().replace("```json", "").replace("```", "").strip()
                    s = clean.find("[")
                    e = clean.rfind("]")
                    if s != -1 and e != -1:
                        tasks = json.loads(clean[s:e+1])
                except Exception:
                    pass

            if not tasks:
                t_str = raw
                for sep in ["\n", ",", " এবং ", " আর ", " তারপর ", " এরপর "]:
                    t_str = t_str.replace(sep, "|")
                tasks = [t.strip() for t in t_str.split("|") if len(t.strip()) > 3]
                tasks = [t for t in tasks if not any(w in t.lower() for w in ["সারাদিনের", "আজকের কাজ", "লিস্ট", "কাজ হলো", "কাজ হল"])]

            saved = self.memory.add_tasks(tasks)
            if saved:
                lines = [f"আমি আপনার আজকের {len(saved)}টি কাজ ডায়েরিতে নোট করে রেখেছি:"]
                for i, t in enumerate(saved, 1):
                    lines.append(f"{i}. {t}")
                lines.append("\nযে কাজটি শেষ করবেন, আমাকে শুধু বলবেন \"আমি অমুক কাজটা শেষ করেছি\"—আমি সাথে সাথে মার্ক করে নেব।")
                return {
                    "success": True,
                    "action": "daily_tasks_added",
                    "reply": "\n".join(lines),
                    "details": f"Added {len(saved)} daily tasks"
                }

        # ────── ২. কাজ শেষ হয়েছে মার্ক করা ──────
        is_done = any(w in low for w in [
            "কাজটা করেছি", "কাজটা করসি", "কাজটা শেষ", "কাজ শেষ", "করে ফেলেছি",
            "করে ফেলছি", "কমপ্লিট করেছি", "কমপ্লিট করসি", "হয়ে গেছে", "হয়ে গেছে",
            "done with", "finished task", "completed task"
        ]) or (any(w in low for w in ["শেষ", "করছি", "করসি", "করেছি", "done"]) and any(w in low for w in ["নম্বর", "নাম্বার", "টাস্ক", "কাজ", "task", "ফটোশপ", "মিটিং", "ক্লায়েন্ট"]))

        if is_done and not any(w in low for w in ["কি কি", "কী কী", "হিসাব"]):
            success, task_name = self.memory.mark_completed(raw)
            if not success and self.ai_brain:
                summary = self.memory.get_tasks_summary()
                if summary["pending"]:
                    prompt = f"""The user said: "{raw}"
Pending tasks: {json.dumps(summary["pending"], ensure_ascii=False)}
Which of the pending tasks did the user just complete?
Return ONLY the exact task string from the list, or "NONE" if no match."""
                    try:
                        ans = self.ai_brain.get_response(prompt).strip().strip('"\'')
                        if ans in summary["pending"]:
                            self.memory.mark_completed(ans)
                            success = True
                            task_name = ans
                    except Exception:
                        pass

            if success:
                summary = self.memory.get_tasks_summary()
                reply = f"দারুণ! \"{task_name}\" সম্পন্ন হিসেবে চিহ্নিত করা হলো। আজকের আর {len(summary['pending'])}টি কাজ বাকি আছে।"
                if not summary["pending"]:
                    reply += " 🎉 অভিনন্দন! আপনার আজকের সব কাজ সম্পন্ন হয়েছে!"
                return {
                    "success": True,
                    "action": "task_completed",
                    "reply": reply,
                    "details": f"Completed: {task_name}"
                }

        # ────── ৩. আজকের কাজের হিসাব / কি কি কাজ ছিল ──────
        is_task_summary = any(w in low for w in [
            "কি কি কাজ ছিল", "কী কী কাজ ছিল", "কি কি কাজ আছে", "কী কী কাজ আছে",
            "কাজের হিসাব", "কতটা কাজ বাকি", "কি কি করছি", "কি কি করসি", "কি কাজ বাকি",
            "আজকে আমার কি কাজ", "কাজের তালিকা", "টাস্ক লিস্ট", "আজকের হিসাব",
            "tasks today", "what did i do today", "my tasks"
        ])

        if is_task_summary:
            summary = self.memory.get_tasks_summary()
            if summary["total"] == 0:
                return {
                    "success": True,
                    "action": "daily_tasks_summary",
                    "reply": "আজকের জন্য এখনো কোনো কাজের তালিকা সেভ করা হয়নি। আপনি মুখে বলুন \"আজকে আমার কাজ হলো...\" এবং আমি সব লিখে রাখবো।",
                    "details": "No tasks found for today"
                }

            lines = [f"📋 আজকের কাজের হিসাব ({summary['date']}):"]
            if summary["completed"]:
                lines.append(f"\n✅ সম্পন্ন কাজ ({len(summary['completed'])}টি):")
                for i, t in enumerate(summary["completed"], 1):
                    lines.append(f"  {i}. {t}")
            else:
                lines.append("\n⏳ এখনো কোনো কাজ সম্পন্ন হয়নি।")

            if summary["pending"]:
                lines.append(f"\n⏳ বাকি কাজ ({len(summary['pending'])}টি):")
                for i, t in enumerate(summary["pending"], 1):
                    lines.append(f"  {i}. {t}")
            else:
                lines.append("\n🎉 সাবাস! আজকের সব কাজ সম্পূর্ণ সম্পন্ন হয়েছে!")

            return {
                "success": True,
                "action": "daily_tasks_summary",
                "reply": "\n".join(lines),
                "details": f"Total: {summary['total']}, Completed: {len(summary['completed'])}, Pending: {len(summary['pending'])}"
            }

        # ────── ৪. দীর্ঘমেয়াদী স্মৃতি সংরক্ষণ ("মনে রাখো...") ──────
        is_remember = any(w in low for w in [
            "মনে রাখো", "মনে রাখিস", "মনে রেখো", "নোট রাখো", "নোট করো", "মনে রাখবা",
            "remember that", "remember this", "save note"
        ])
        if is_remember:
            clean_fact = raw
            for stop in ["মনে রাখো যে", "মনে রাখিস যে", "মনে রেখো যে", "মনে রাখো", "মনে রাখিস", "মনে রেখো", "নোট রাখো", "নোট করো", "remember that", "remember this"]:
                clean_fact = clean_fact.replace(stop, "")
            clean_fact = clean_fact.strip(" :,-")
            if clean_fact:
                self.memory.remember(clean_fact)
                return {
                    "success": True,
                    "action": "memory_saved",
                    "reply": f"আমি স্মৃতিতে সংরক্ষণ করে রাখলাম: \"{clean_fact}\"। আপনি যেকোনো সময় জিজ্ঞেস করলে আমি সাথে সাথে বলে দেব।",
                    "details": f"Saved memory: {clean_fact}"
                }

        # ────── ৫. স্মৃতি স্মরণ ("মনে আছে...") ──────
        is_recall = any(w in low for w in [
            "মনে আছে", "কী বলেছিলাম", "কি বলেছিলাম", "নোট দেখো", "নোট বলো", "স্মৃতিতে কি আছে",
            "do you remember", "what did i tell you"
        ])
        if is_recall:
            recalled = self.memory.recall(raw)
            if recalled:
                mem_texts = [r["content"] for r in recalled]
                return {
                    "success": True,
                    "action": "memory_recalled",
                    "reply": f"হ্যাঁ, আমার মনে আছে! আপনার সংরক্ষিত নোট হলো: {', '.join(mem_texts)}",
                    "details": "Recalled memories from SQLite"
                }

        return None

    # ══════════════════════════════════════════════════
    # 🤖 AI-Directed Universal Execution (Gemini)
    # ══════════════════════════════════════════════════
    def _ai_directed_execution(self, user_command: str) -> dict:
        if not self.ai_brain:
            return {"success": False, "action": "ai",
                    "reply": "AI ব্রেন সংযুক্ত নেই।", "details": "No AI brain"}

        context = ""
        if hasattr(self, 'memory') and self.memory:
            context = self.memory.get_ai_memory_context()

        prompt = f"""You are JARVIS, an autonomous Windows PC controller and intelligent voice assistant.
The user gave this instruction or question in Bengali or English: "{user_command}"

Context about the user and their day:
{context}

You have full control of Windows 10/11. Generate the exact action to accomplish whatever the user asks.

Respond with a JSON object ONLY:
{{
  "intent": "powershell" | "python" | "open_url" | "conversation",
  "command": "Windows PowerShell command or Python snippet or URL or null",
  "reply_bengali": "Short natural Bengali spoken reply answering the question or confirming what you are doing (1-2 sentences)"
}}

Guidelines:
- For PC actions (open any app, folder, file, settings, audio, wifi, Bluetooth, window management, system commands): use "powershell" intent with safe, valid commands.
- For simulating mouse/keyboard combos (e.g. shortcut keys, typing into active window): use "python" with pyautogui.
- For browsing websites or searching: use "open_url".
- For answering questions, calculations, general knowledge, or conversational chat: use "conversation" with an intelligent Bengali answer in "reply_bengali".
- Keep "reply_bengali" concise, accurate and natural for voice speaking."""

        try:
            raw = self.ai_brain.get_response(prompt)
            clean = (raw or "").strip()

            # Clean JSON formatting
            if "```json" in clean:
                clean = clean.split("```json")[1].split("```")[0].strip()
            elif "```" in clean:
                clean = clean.split("```")[1].split("```")[0].strip()

            data = {}
            try:
                data = json.loads(clean)
            except Exception:
                # Find outermost JSON object
                start = clean.find("{")
                end = clean.rfind("}")
                if start != -1 and end != -1:
                    data = json.loads(clean[start:end+1])

            intent = data.get("intent", "conversation")
            cmd    = data.get("command")
            reply  = data.get("reply_bengali") or data.get("spoken_reply_bengali") or "কাজটি করা হচ্ছে।"

            if intent == "powershell" and cmd:
                proc = subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                    capture_output=True, text=True, timeout=20
                )
                output = (proc.stdout or "").strip()
                details = f"PowerShell: {cmd}"
                if output and len(output) < 150 and any(k in user_command for k in ["কত", "কি", "কী", "দেখাও", "বলো", "তথ্য"]):
                    reply = f"{reply} {output}".strip()

            elif intent == "python" and cmd:
                proc = subprocess.run(
                    [sys.executable, "-c", cmd],
                    capture_output=True, text=True, timeout=15
                )
                details = f"Python: {cmd}"

            elif intent == "open_url" and cmd:
                self._open_url(cmd)
                details = f"URL: {cmd}"

            else:
                # General conversation or information query
                details = f"Conversation: {reply}"

            if hasattr(self, 'memory') and self.memory:
                self.memory.log_chat("user", user_command)
                self.memory.log_chat("assistant", reply)

            return {"success": True, "action": intent, "reply": reply, "details": details}

        except Exception as e:
            # Fallback — যদি কোনো কারণে AI এক্সেকিউশন আটকে যায়
            fallback_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(user_command)}"
            self._open_url(fallback_url)
            return {
                "success": True,
                "action": "web_search",
                "reply": f"\"{user_command}\" সম্পর্কে গুগলে সার্চ করা হচ্ছে।",
                "details": str(e)
            }


    # ══════════════════════════════════════════════════
    # 🔐 Facebook Auto-Login System
    # ══════════════════════════════════════════════════

    def _facebook_login_start(self, raw: str) -> dict:
        """Facebook খুলে login field এ ফোকাস করো।"""
        import time
        self._open_url("https://www.facebook.com")
        time.sleep(3.5)  # পেজ লোড হওয়ার জন্য অপেক্ষা

        # Email field এ ক্লিক করো
        try:
            if pyautogui:
                # Tab দিয়ে email field এ যাও (Facebook layout: email field প্রথম)
                pyautogui.hotkey('ctrl', 'l')   # Address bar clear
                import time; time.sleep(0.3)
                pyautogui.hotkey('escape')
                time.sleep(0.3)
                # Page এর email input এ ক্লিক করো (approximate position)
                pyautogui.click(760, 400)  # Screen center area
                time.sleep(0.5)
                # Tab দিয়ে email field খোঁজো
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('tab')
                pyautogui.press('tab')
        except Exception:
            pass

        return {
            "success": True,
            "action": "facebook_login_start",
            "reply": "ফেসবুক খুলছি। পেজ লোড হলে আপনার নম্বর বলুন — বলুন 'নম্বর হলো 01XXXXXXXXX'",
            "details": "Facebook opened, waiting for number"
        }

    def _type_in_active_field(self, value: str, field_type: str) -> dict:
        """Active field এ value টাইপ করো।"""
        import time
        try:
            if pyautogui:
                import pyperclip
                # Active field এ ভ্যালু পেস্ট করো
                pyperclip.copy(value)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.3)
                # Tab চেপে পাসওয়ার্ড ফিল্ডে যাও
                pyautogui.press('tab')

                return {
                    "success": True,
                    "action": "type_phone",
                    "reply": f"নম্বর {value} বসানো হয়েছে। এখন পাসওয়ার্ড বলুন — যেমন 'পাসওয়ার্ড হলো আপনার_পাসওয়ার্ড'।",
                    "details": f"Typed: {value} and tabbed"
                }
        except Exception as e:
            pass

        return {
            "success": False,
            "action": "type_phone",
            "reply": "টাইপ করতে সমস্যা হয়েছে।",
            "details": "pyautogui error"
        }

    def _type_password_and_login(self, password: str) -> dict:
        """Password টাইপ করো।"""
        import time
        try:
            if pyautogui:
                import pyperclip
                pyperclip.copy(password)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.3)

                return {
                    "success": True,
                    "action": "facebook_login",
                    "reply": "পাসওয়ার্ড বসানো হয়েছে। লগইন করতে 'লগইন করো' বলুন অথবা এন্টার চাপুন।",
                    "details": "Password entered"
                }
        except Exception:
            pass

        return {
            "success": False,
            "action": "facebook_login",
            "reply": "পাসওয়ার্ড টাইপ করতে সমস্যা হয়েছে।",
            "details": "pyautogui error"
        }

    def _calculate_and_type_math(self, raw: str, low: str) -> dict:
        """গাণিতিক হিসাব সমাধান করে এবং ক্যালকুলেটর বা স্ক্রিনে লাইভ টাইপ করে।"""
        import re
        import time
        bn_digits = {'০':'0', '১':'1', '২':'2', '৩':'3', '৪':'4', '৫':'5', '৬':'6', '৭':'7', '৮':'8', '৯':'9'}
        clean = raw
        for bn, en in bn_digits.items():
            clean = clean.replace(bn, en)

        replacements = [
            ("হিসাব করো", ""), ("হিসাব", ""), ("calculate", ""), ("কত হয়", ""), ("কত হয়", ""),
            ("গুণন", "*"), ("গুণ", "*"), ("গুন", "*"), ("ইনটু", "*"), ("times", "*"), ("into", "*"), ("x", "*"),
            ("প্লাস", "+"), ("যোগ", "+"), ("plus", "+"),
            ("বিয়োগ", "-"), ("মাইনাস", "-"), ("minus", "-"),
            ("ভাগ", "/"), ("ডিভাইডেড", "/"), ("divided by", "/"), ("divided", "/")
        ]
        expr = clean.lower()
        for w, r in replacements:
            expr = expr.replace(w, r)

        # শুধু গাণিতিক চিহ্ন রাখুন
        math_chars = re.findall(r'[\d\+\-\*\/\.\(\)\s]+', expr)
        math_expr = ''.join(math_chars).strip()

        if not math_expr or not any(c.isdigit() for c in math_expr):
            return {"success": False, "reply": "সঠিক সংখ্যা বুঝতে পারিনি।"}

        try:
            val = eval(math_expr, {"__builtins__": None}, {})
            if isinstance(val, float) and val.is_integer():
                val = int(val)

            # স্ক্রিনে বা ক্যালকুলেটরে লাইভ টাইপিং
            if pyautogui:
                time.sleep(0.3)
                for char in math_expr:
                    pyautogui.press(char if char in "0123456789+-*/." else "space")
                    time.sleep(0.04)
                pyautogui.press('enter')

            return {
                "success": True,
                "action": "calculate",
                "reply": f"হিসাব সম্পন্ন হয়েছে। {math_expr} এর উত্তর হলো {val}।",
                "details": f"{math_expr} = {val}"
            }
        except Exception as e:
            return {"success": False, "reply": f"হিসাব করতে ত্রুটি: {e}"}

    def _handle_antigravity_action(self, raw: str, low: str) -> dict:
        """Antigravity IDE সামনে আনে এবং চ্যাট বক্সে মেসেজ লিখে পাঠায়।"""
        import time
        # Antigravity IDE সামনে আনো
        ag_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Antigravity IDE\Antigravity IDE.exe"),
            r"C:\Users\Admin\AppData\Local\Programs\Antigravity IDE\Antigravity IDE.exe",
        ]
        for p in ag_paths:
            if os.path.exists(p):
                try:
                    os.startfile(p)
                    break
                except Exception:
                    pass

        time.sleep(1.0)

        # চ্যাটে লেখার কোনো টেক্সট আছে কিনা দেখো
        msg = ""
        for trig in ["চ্যাট বক্সে লেখো", "চ্যাট বক্সে লেখ", "চ্যাটে লেখো", "চ্যাটে লেখ", "চ্যাটবক্সে লেখো", "চ্যাটবক্সে লেখ", "এন্টিগ্র্যাভিটিতে লেখো", "এন্টিগ্র্যাভিটিতে লেখ", "লেখো", "লেখ"]:
            if trig in low:
                idx = low.find(trig) + len(trig)
                msg = raw[idx:].strip().strip(":=- ")
                msg = msg.lstrip("ো ").strip()
                for send_w in ["এবং পাঠাও", "পাঠাও", "সেন্ড করো", "send koro", "পাঠিয়ে দাও"]:
                    if send_w in msg.lower():
                        msg = msg[:msg.lower().find(send_w)].strip()
                break

        if msg and pyautogui:
            import pyperclip
            # Ctrl + L দিয়ে Antigravity AI চ্যাট বক্স ফোকাস করো
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)
            pyperclip.copy(msg)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            if any(w in low for w in ["পাঠাও", "সেন্ড", "send", "পাঠিয়ে দাও"]):
                pyautogui.press('enter')
                return {
                    "success": True,
                    "action": "antigravity_chat",
                    "reply": f"অ্যান্টিগ্র্যাভিটি চ্যাটে লিখে পাঠানো হয়েছে: {msg}",
                    "details": f"Sent to Antigravity: {msg}"
                }
            else:
                return {
                    "success": True,
                    "action": "antigravity_chat",
                    "reply": f"অ্যান্টিগ্র্যাভিটি চ্যাটে লেখা হয়েছে: {msg}",
                    "details": f"Typed into Antigravity: {msg}"
                }

        return {
            "success": True,
            "action": "antigravity_open",
            "reply": "অ্যান্টিগ্র্যাভিটি উইন্ডো আপনার সামনে সক্রিয় করা হয়েছে।",
            "details": "Activated Antigravity IDE"
        }

    def _selenium_facebook_login(self, phone: str, password: str) -> dict:
        """
        Selenium দিয়ে Facebook-এ ফোন নম্বর ও পাসওয়ার্ড দিয়ে লগইন করো।
        এটি সবচেয়ে নির্ভরযোগ্য পদ্ধতি।
        """
        import time
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options

            opts = Options()
            opts.add_argument("--start-maximized")
            opts.add_experimental_option("detach", True)  # browser খোলা থাকবে
            driver = webdriver.Chrome(options=opts)

            driver.get("https://www.facebook.com")
            wait = WebDriverWait(driver, 10)

            # Email/Phone field
            email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_field.clear()
            email_field.send_keys(phone)
            time.sleep(0.5)

            # Password field
            pass_field = driver.find_element(By.ID, "pass")
            pass_field.clear()
            pass_field.send_keys(password)
            time.sleep(0.5)

            # Login button
            login_btn = driver.find_element(By.NAME, "login")
            login_btn.click()

            return {
                "success": True,
                "action": "facebook_login",
                "reply": f"ফেসবুকে {phone} দিয়ে লগইন করা হচ্ছে!",
                "details": f"Selenium login: {phone}"
            }

        except ImportError:
            return {
                "success": False,
                "action": "facebook_login",
                "reply": "Selenium ইনস্টল নেই। 'pip install selenium' চালাও।",
                "details": "selenium not installed"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "facebook_login",
                "reply": f"লগইনে সমস্যা হয়েছে: {str(e)[:50]}",
                "details": str(e)
            }


    # ══════════════════════════════════════════════════
    # 📱 WhatsApp Folder & Media Automation
    # ══════════════════════════════════════════════════

    def _handle_folder_to_whatsapp(self, raw: str, low: str) -> dict:
        """
        ডি ড্রাইভ বা যেকোনো ফোল্ডার থেকে ছবি/ফাইল খুঁজে হোয়াটসঅ্যাপে নির্দিষ্ট ব্যক্তিকে স্বয়ংক্রিয়ভাবে পাঠানো।
        ব্যবহারকারী যেমন বলে:
        'file manager open koro kore d drive a giye amar all photo file ar moddhe j j image ase sob amar md rakib name a whatsapp a send koro'
        """
        import re
        import time

        print(f"[*] Processing WhatsApp Media Transfer: {raw}", flush=True)

        # ১. ড্রাইভ শনাক্তকরণ (Default 'D')
        drive_match = re.search(r'([a-zA-Z])\s*(?:drive|ড্রাইভ|:)', low)
        drive_letter = drive_match.group(1).upper() if drive_match else "D"
        drive_root = f"{drive_letter}:\\"

        # ২. কনট্যাক্ট বা প্রাপকের নাম শনাক্তকরণ (হোয়াটসঅ্যাপ শব্দের আগের অংশ বিশ্লেষণ)
        contact_name = ""
        wa_idx = low.find('whatsapp')
        if wa_idx == -1:
            wa_idx = low.find('হোয়াটসঅ্যাপ')
        if wa_idx == -1:
            wa_idx = low.find('হোয়াটসঅ্যাপ')

        if wa_idx != -1:
            before_wa = raw[:wa_idx].strip()
            for marker in ['name a', 'name', 'নামে', 'নামের', ' k', ' কে', ' k ', ' কে ']:
                m_idx = before_wa.lower().rfind(marker)
                if m_idx != -1:
                    cand = before_wa[:m_idx].strip()
                    for lead in ['sob amar', 'amar', 'সব আমার', 'আমার', 'to ', 'send to ']:
                        l_idx = cand.lower().rfind(lead)
                        if l_idx != -1:
                            cand = cand[l_idx + len(lead):].strip()
                    words = cand.split()
                    if len(words) > 3:
                        cand = ' '.join(words[-3:])
                    contact_name = cand
                    break

        if not contact_name:
            # প্যাটার্ন: 'whatsapp a md rakib k'
            m2 = re.search(r'(?:whatsapp|হোয়াটসঅ্যাপ|হোয়াটসঅ্যাপ)[^\w]+(?:a|এ|te|তে)?\s+([a-zA-Z0-9\u0980-\u09FF\s\.]+?)(?:\s+(?:k|কে|name|নামে|send|পাঠাও|দাও|sed)|$)', raw, re.IGNORECASE)
            if m2:
                contact_name = m2.group(1).strip()

        # ৩. ফোল্ডারের নাম শনাক্তকরণ
        folder_query = ""
        # প্যাটার্ন: 'd drive a giye amar all photo file ar moddhe'
        m_f = re.search(r'(?:drive|ড্রাইভ)[^\w]+(?:a|এ|er|এর|giye|গিয়ে)?\s*(?:amar|আমার)?\s*(.+?)\s*(?:file|ফাইল|folder|ফোল্ডার|এর\s*মধ্যে|ar\s*moddhe)', low)
        if m_f:
            folder_query = m_f.group(1).strip()
        
        if not folder_query:
            m_f2 = re.search(r'(?:giye|গিয়ে)\s+(?:amar|আমার)?\s*(.+?)\s+(?:file|ফাইল|folder|ফোল্ডার)', low)
            if m_f2:
                folder_query = m_f2.group(1).strip()

        for s in ["giye", "গিয়ে", "amar", "আমার", "d drive a", "d drive", "drive a", "ড্রাইভে"]:
            folder_query = folder_query.replace(s, "").strip()

        # ফলব্যাক যদি এখনও ফাঁকা থাকে
        if not folder_query or folder_query == "":
            folder_query = "all photo"
        if not contact_name or contact_name == "":
            contact_name = "md rakib"

        # ৪. ফোল্ডার খুঁজে বের করা
        target_dir = None
        if os.path.exists(drive_root):
            direct_check = os.path.join(drive_root, folder_query)
            if os.path.exists(direct_check) and os.path.isdir(direct_check):
                target_dir = direct_check
            else:
                try:
                    for item in os.listdir(drive_root):
                        full = os.path.join(drive_root, item)
                        if os.path.isdir(full):
                            norm_item = item.lower().replace("_", " ").replace("-", " ")
                            norm_query = folder_query.lower().replace("_", " ").replace("-", " ")
                            if norm_query in norm_item or norm_item in norm_query or ("photo" in norm_query and "photo" in norm_item):
                                target_dir = full
                                break
                except Exception as e:
                    print(f"[Folder Search Error]: {e}", flush=True)

        if not target_dir or not os.path.exists(target_dir):
            target_dir = os.path.join(drive_root, folder_query)
            try:
                os.makedirs(target_dir, exist_ok=True)
            except Exception:
                target_dir = drive_root

        # ৫. ফাইল এক্সপ্লোরার ওপেন করে দেখানো
        try:
            subprocess.Popen(["explorer.exe", target_dir])
        except Exception:
            pass

        # ৬. ফোল্ডার থেকে ছবি সংগ্রহ করা
        image_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heic"}
        image_files = []
        if os.path.exists(target_dir):
            for root, _, files in os.walk(target_dir):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in image_exts:
                        image_files.append(os.path.join(root, f))
                if image_files:
                    break

        if not image_files:
            return {
                "success": True,
                "action": "open_folder",
                "reply": f"ফাইল ম্যানেজারে {drive_letter} ড্রাইভের '{os.path.basename(target_dir)}' ফোল্ডার খোলা হয়েছে, তবে এতে কোনো ছবি পাওয়া যায়নি। ছবি রেখে পুনরায় বলুন।",
                "details": f"Opened {target_dir}, but 0 images found"
            }

        # ৭. উইন্ডোজ ক্লিপবোর্ডে ছবিগুলো কপি করা (PowerShell Set-Clipboard)
        try:
            paths_str = ",".join(f"'{p}'" for p in image_files[:15])
            ps_cmd = f"Set-Clipboard -Path {paths_str}"
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, timeout=5)
        except Exception as e:
            print(f"[Clipboard Set Error]: {e}", flush=True)

        # ৮. হোয়াটসঅ্যাপ লঞ্চ করা
        try:
            subprocess.Popen("start whatsapp:", shell=True)
        except Exception:
            self._open_url("https://web.whatsapp.com")
        
        time.sleep(2.5)

        # ৯. PyAutoGUI দিয়ে স্বয়ংক্রিয়ভাবে সার্চ, ওপেন ও ছবি সেন্ড
        try:
            import pyautogui
            import pyperclip
            pyautogui.FAILSAFE = False

            # সার্চ বারে ফোকাস (Ctrl + F)
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.6)

            # নাম পেস্ট ও সার্চ
            pyperclip.copy(contact_name)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)

            # চ্যাট সিলেক্ট (Enter)
            pyautogui.press('enter')
            time.sleep(1.2)

            # ছবি পেস্ট (Ctrl + V)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2.0)

            # সেন্ড বাটনে ক্লিক বা Enter
            pyautogui.press('enter')
            time.sleep(0.5)

        except Exception as e:
            print(f"[Automation Error]: {e}", flush=True)

        folder_name_disp = os.path.basename(target_dir)
        return {
            "success": True,
            "action": "send_folder_to_whatsapp",
            "reply": f"ফাইল ম্যানেজার থেকে {drive_letter} ড্রাইভের {folder_name_disp} ফোল্ডারে গিয়ে {len(image_files)}টি ছবি হোয়াটসঅ্যাপে {contact_name}-কে পাঠানো হয়েছে।",
            "details": f"Sent {len(image_files)} images from {target_dir} to WhatsApp contact: {contact_name}"
        }
