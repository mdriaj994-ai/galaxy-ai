"""
JARVIS Command Processor — Full Voice PC Control
বাংলা ও ইংরেজিতে যেকোনো PC কমান্ড পরিচালনা করে।
মাউস, কীবোর্ড, অ্যাপ, ফাইল, ওয়েব — সব কিছু ভয়েসে।
"""

import os
import re
import sys
import ast
import time
import glob
import random
import datetime
import platform
import operator
import threading
import subprocess
import webbrowser
import urllib.parse
from pathlib import Path

# pyautogui safe import
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# ctypes (Windows native)
try:
    import ctypes
    HAS_CTYPES = True
except ImportError:
    HAS_CTYPES = False


class CommandProcessor:
    """সব ধরনের সিস্টেম কমান্ড প্রসেস করে — বাংলা ও ইংরেজি।"""

    def __init__(self, settings, assistant):
        self.settings = settings
        self.assistant = assistant
        self.os = platform.system().lower()

    # ══════════════════════════════════════════
    # 🎯 MAIN PROCESSOR
    # ══════════════════════════════════════════

    def process(self, command: str) -> bool:
        """
        কমান্ড প্রসেস করো।
        Returns True যদি কমান্ডটি handle করা হয়।
        """
        cmd = command.lower().strip()

        # ── সময় ও তারিখ ──────────────────────────
        if self._m(cmd, ["সময় কত", "কয়টা বাজে", "এখন কটা", "সময় বলো", "টাইম বলো",
                         "what time", "current time", "time is it", "what's the time"]):
            self._tell_time(); return True

        if self._m(cmd, ["আজ কত তারিখ", "তারিখ কত", "আজকের তারিখ", "তারিখ বলো",
                         "what date", "today's date", "current date", "what's the date"]):
            self._tell_date(); return True

        if self._m(cmd, ["কি বার", "কোন দিন", "আজকের দিন", "আজ কি বার",
                         "what day", "day is it", "which day"]):
            self._tell_day(); return True

        # ── ওয়েব সার্চ ───────────────────────────
        for prefix in ["গুগলে সার্চ করো ", "গুগলে সার্চ কর ", "গুগলে খোঁজো ",
                        "search for ", "search ", "google "]:
            if cmd.startswith(prefix):
                self._search_google(cmd[len(prefix):].strip()); return True

        for prefix in ["ইউটিউবে সার্চ করো ", "ইউটিউবে দেখাও ", "ইউটিউবে বাজাও ",
                       "youtube ", "play on youtube ", "search youtube "]:
            if cmd.startswith(prefix):
                self._search_youtube(cmd[len(prefix):].strip()); return True

        if self._m(cmd, ["ইউটিউব চালু করো", "ইউটিউব খোলো", "open youtube"]):
            self._open_website("youtube"); return True

        for prefix in ["open website ", "go to ", "ওয়েবসাইট খোলো ", "ওয়েবসাইটে যাও "]:
            if cmd.startswith(prefix):
                self._open_website(cmd[len(prefix):].strip()); return True

        # ── অ্যাপ খোলা/বন্ধ ──────────────────────
        for prefix in ["open ", "খোলো ", "চালু করো ", "চালু কর "]:
            if cmd.startswith(prefix):
                name = cmd[len(prefix):].strip()
                return self._open_app_or_site(name)
            # Middle-of-sentence matching (e.g. "আমার ক্রোমটা খোলো")
            if prefix.strip() in cmd:
                idx = cmd.find(prefix.strip())
                name = cmd[idx + len(prefix.strip()):].strip()
                if name:
                    return self._open_app_or_site(name)

        for prefix in ["close ", "বন্ধ করো ", "বন্ধ কর ", "kill "]:
            if cmd.startswith(prefix):
                name = cmd[len(prefix):].strip()
                return self._close_app(name)
            if prefix.strip() in cmd:
                idx = cmd.find(prefix.strip())
                name = cmd[idx + len(prefix.strip()):].strip()
                if name:
                    return self._close_app(name)

        # ── মাউস কন্ট্রোল ─────────────────────────
        if self._m(cmd, ["মাউস উপরে", "mouse up", "move mouse up"]):
            self._mouse_move(0, -100); return True
        if self._m(cmd, ["মাউস নিচে", "mouse down", "move mouse down"]):
            self._mouse_move(0, 100); return True
        if self._m(cmd, ["মাউস বামে", "mouse left", "move mouse left"]):
            self._mouse_move(-100, 0); return True
        if self._m(cmd, ["মাউস ডানে", "mouse right", "move mouse right"]):
            self._mouse_move(100, 0); return True
        if self._m(cmd, ["ক্লিক করো", "ক্লিক কর", "mouse click", "click"]):
            self._mouse_click(); return True
        if self._m(cmd, ["ডাবল ক্লিক", "double click"]):
            self._mouse_double_click(); return True
        if self._m(cmd, ["রাইট ক্লিক", "right click"]):
            self._mouse_right_click(); return True
        if self._m(cmd, ["স্ক্রল আপ", "scroll up", "উপরে স্ক্রল"]):
            self._scroll(3); return True
        if self._m(cmd, ["স্ক্রল ডাউন", "scroll down", "নিচে স্ক্রল"]):
            self._scroll(-3); return True

        # ── কীবোর্ড কন্ট্রোল ──────────────────────
        for prefix in ["টাইপ করো ", "type ", "লেখো ", "লিখো "]:
            if cmd.startswith(prefix):
                text = command[len(prefix):].strip()  # original case
                self._type_text(text); return True

        if self._m(cmd, ["এন্টার চাপো", "এন্টার দাও", "press enter", "enter"]):
            self._press_key("enter"); return True
        if self._m(cmd, ["ব্যাকস্পেস", "backspace", "মুছে দাও"]):
            self._press_key("backspace"); return True
        if self._m(cmd, ["escape", "esc", "এস্কেপ", "বাতিল"]):
            self._press_key("escape"); return True
        if self._m(cmd, ["tab চাপো", "press tab", "ট্যাব"]):
            self._press_key("tab"); return True
        if self._m(cmd, ["space চাপো", "press space", "স্পেস দাও"]):
            self._press_key("space"); return True
        if self._m(cmd, ["delete চাপো", "press delete", "ডিলেট"]):
            self._press_key("delete"); return True

        # ── উইন্ডো কন্ট্রোল ──────────────────────
        if self._m(cmd, ["উইন্ডো মিনিমাইজ", "minimize", "মিনিমাইজ করো", "ছোট করো"]):
            self._window_minimize(); return True
        if self._m(cmd, ["উইন্ডো ম্যাক্সিমাইজ", "maximize", "ম্যাক্সিমাইজ করো", "বড় করো"]):
            self._window_maximize(); return True
        if self._m(cmd, ["উইন্ডো বন্ধ", "close window", "জানালা বন্ধ"]):
            self._window_close(); return True
        if self._m(cmd, ["সব মিনিমাইজ", "minimize all", "ডেস্কটপ দেখাও", "show desktop"]):
            self._minimize_all(); return True
        if self._m(cmd, ["পরবর্তী উইন্ডো", "switch window", "alt tab", "উইন্ডো বদলাও"]):
            self._alt_tab(); return True
        if self._m(cmd, ["উইন্ডো রিফ্রেশ", "refresh", "রিফ্রেশ"]):
            self._press_key("f5"); return True

        # ── ট্যাব কন্ট্রোল (ব্রাউজার) ─────────────
        if self._m(cmd, ["নতুন ট্যাব", "new tab", "নতুন পেজ"]):
            self._hotkey("ctrl", "t"); return True
        if self._m(cmd, ["ট্যাব বন্ধ", "close tab"]):
            self._hotkey("ctrl", "w"); return True
        if self._m(cmd, ["পরের ট্যাব", "next tab"]):
            self._hotkey("ctrl", "tab"); return True
        if self._m(cmd, ["আগের ট্যাব", "previous tab", "prev tab"]):
            self._hotkey("ctrl", "shift", "tab"); return True
        if self._m(cmd, ["পেজ রিলোড", "reload page", "পেজ রিফ্রেশ"]):
            self._hotkey("ctrl", "r"); return True

        # ── কপি/পেস্ট/কাট ────────────────────────
        if self._m(cmd, ["কপি করো", "copy", "কপি"]):
            self._hotkey("ctrl", "c"); return True
        if self._m(cmd, ["পেস্ট করো", "paste", "পেস্ট"]):
            self._hotkey("ctrl", "v"); return True
        if self._m(cmd, ["কাট করো", "cut", "কাট"]):
            self._hotkey("ctrl", "x"); return True
        if self._m(cmd, ["সব সিলেক্ট", "select all"]):
            self._hotkey("ctrl", "a"); return True
        if self._m(cmd, ["আনডু", "undo", "পূর্বাবস্থা"]):
            self._hotkey("ctrl", "z"); return True
        if self._m(cmd, ["রিডু", "redo"]):
            self._hotkey("ctrl", "y"); return True
        if self._m(cmd, ["সেভ করো", "save", "সংরক্ষণ"]):
            self._hotkey("ctrl", "s"); return True
        if self._m(cmd, ["প্রিন্ট করো", "print", "প্রিন্ট"]):
            self._hotkey("ctrl", "p"); return True
        if self._m(cmd, ["ফাইন্ড করো", "find", "খোঁজো"]):
            self._hotkey("ctrl", "f"); return True

        # ── সিস্টেম কমান্ড ────────────────────────
        if self._m(cmd, ["স্ক্রিনশট নাও", "স্ক্রিনশট করো", "screenshot", "take screenshot"]):
            self._take_screenshot(); return True
        if self._m(cmd, ["স্ক্রিন লক", "lock screen", "lock computer", "কম্পিউটার লক"]):
            self._lock_screen(); return True
        if self._m(cmd, ["শাটডাউন", "shutdown", "কম্পিউটার বন্ধ করো", "পিসি বন্ধ"]):
            self._shutdown(); return True
        if self._m(cmd, ["রিস্টার্ট", "restart", "reboot", "কম্পিউটার রিস্টার্ট"]):
            self._restart(); return True
        if self._m(cmd, ["স্লিপ", "sleep", "ঘুম মোড", "hibernate"]):
            self._sleep(); return True
        if self._m(cmd, ["টাস্ক ম্যানেজার", "task manager"]):
            subprocess.Popen("taskmgr.exe", shell=True)
            self.assistant.speak("টাস্ক ম্যানেজার চালু হচ্ছে।"); return True
        if self._m(cmd, ["সেটিংস খোলো", "settings", "উইন্ডোজ সেটিংস"]):
            subprocess.Popen("start ms-settings:", shell=True)
            self.assistant.speak("সেটিংস খোলা হচ্ছে।"); return True
        if self._m(cmd, ["রিসাইকেল বিন খালি", "empty recycle bin", "ট্র্যাশ খালি"]):
            self._empty_recycle_bin(); return True

        # ── ভলিউম কন্ট্রোল ─────────────────────────
        if self._m(cmd, ["ভলিউম বাড়াও", "আওয়াজ বাড়াও", "volume up", "louder"]):
            self._volume_change("up"); return True
        if self._m(cmd, ["ভলিউম কমাও", "আওয়াজ কমাও", "volume down", "quieter"]):
            self._volume_change("down"); return True
        if self._m(cmd, ["মিউট করো", "মিউট", "mute", "আওয়াজ বন্ধ"]):
            self._mute(); return True
        if self._m(cmd, ["আনমিউট", "unmute", "আওয়াজ চালু"]):
            self._mute(); return True  # toggle

        # নির্দিষ্ট ভলিউম
        vol_match = re.search(r'ভলিউম\s*(\d+)|volume\s*(\d+)', cmd)
        if vol_match:
            level = int(vol_match.group(1) or vol_match.group(2))
            self._set_volume(level); return True

        # ── মিডিয়া কন্ট্রোল ──────────────────────
        if self._m(cmd, ["গান বাজাও", "play", "প্লে", "মিউজিক চালু"]):
            self._media_play_pause(); return True
        if self._m(cmd, ["গান থামাও", "pause", "পজ", "মিউজিক থামাও"]):
            self._media_play_pause(); return True
        if self._m(cmd, ["পরবর্তী গান", "next song", "next track"]):
            self._media_next(); return True
        if self._m(cmd, ["আগের গান", "previous song", "prev track"]):
            self._media_previous(); return True

        # ── ব্রাইটনেস ─────────────────────────────
        if self._m(cmd, ["স্ক্রিন উজ্জ্বল করো", "brightness up", "ব্রাইটনেস বাড়াও"]):
            self._brightness("up"); return True
        if self._m(cmd, ["স্ক্রিন অন্ধকার", "brightness down", "ব্রাইটনেস কমাও"]):
            self._brightness("down"); return True

        # ── ফাইল ও ফোল্ডার ──────────────────────
        if self._m(cmd, ["ডাউনলোড খোলো", "open downloads"]):
            self._open_folder("downloads"); return True
        if self._m(cmd, ["ডকুমেন্ট খোলো", "open documents"]):
            self._open_folder("documents"); return True
        if self._m(cmd, ["ডেস্কটপ খোলো", "open desktop"]):
            self._open_folder("desktop"); return True
        if self._m(cmd, ["পিকচার খোলো", "open pictures", "ছবি খোলো"]):
            self._open_folder("pictures"); return True
        if self._m(cmd, ["মিউজিক ফোল্ডার", "open music"]):
            self._open_folder("music"); return True
        if self._m(cmd, ["ভিডিও ফোল্ডার", "open videos"]):
            self._open_folder("videos"); return True

        # ── ক্যালকুলেশন ──────────────────────────
        if self._m(cmd, ["হিসাব করো", "calculate", "compute", "কত হয়"]):
            result = self._calculate(cmd)
            if result: return True

        # ── সিস্টেম তথ্য ──────────────────────────
        if self._m(cmd, ["আইপি", "ip address", "my ip", "আমার আইপি"]):
            self._system_info(); return True
        if self._m(cmd, ["ব্যাটারি", "battery", "চার্জ কত"]):
            self._battery_info(); return True
        if self._m(cmd, ["র‍্যাম ব্যবহার", "ram usage", "memory usage"]):
            self._ram_info(); return True
        if self._m(cmd, ["সিপিইউ ব্যবহার", "cpu usage"]):
            self._cpu_info(); return True
        if self._m(cmd, ["ডিস্ক স্পেস", "disk space", "storage"]):
            self._disk_info(); return True

        # ── মজার কমান্ড ──────────────────────────
        if self._m(cmd, ["জোকস বলো", "tell me a joke", "joke"]):
            self._tell_joke(); return True
        if self._m(cmd, ["কয়েন ফ্লিপ", "flip a coin", "coin flip"]):
            self._flip_coin(); return True
        if self._m(cmd, ["ডাইস রোল", "roll dice", "dice"]):
            self._roll_dice(); return True
        if self._m(cmd, ["র‍্যান্ডম নম্বর", "random number"]):
            self._random_number(); return True

        # ── ইতিহাস মুছো ──────────────────────────
        if self._m(cmd, ["ইতিহাস মুছো", "clear history", "রিসেট", "forget everything"]):
            self._clear_history(); return True

        return False

    # ══════════════════════════════════════════
    # 📅 সময় ও তারিখ
    # ══════════════════════════════════════════

    def _tell_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.assistant.speak(f"এখন সময় হলো {time_str}।")

    def _tell_date(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%d %B %Y")
        self.assistant.speak(f"আজকের তারিখ হলো {date_str}।")

    def _tell_day(self):
        days = {
            0: "সোমবার", 1: "মঙ্গলবার", 2: "বুধবার",
            3: "বৃহস্পতিবার", 4: "শুক্রবার",
            5: "শনিবার", 6: "রবিবার"
        }
        day = days.get(datetime.datetime.now().weekday(), "")
        self.assistant.speak(f"আজ {day}।")

    # ══════════════════════════════════════════
    # 🌐 ওয়েব কমান্ড
    # ══════════════════════════════════════════

    def _search_google(self, query: str):
        if not query:
            self.assistant.speak("কী সার্চ করবো বলো।")
            return
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        webbrowser.open(url)
        self.assistant.speak(f"গুগলে {query} সার্চ করা হচ্ছে।")

    def _search_youtube(self, query: str):
        if not query:
            self.assistant.speak("কোন গান বা ভিডিও চাও বলো।")
            return
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
        webbrowser.open(url)
        self.assistant.speak(f"ইউটিউবে {query} খোঁজা হচ্ছে।")

    def _open_website(self, site: str):
        if not site:
            self.assistant.speak("কোন ওয়েবসাইট খুলবো বলো।")
            return
        sites = {
            "facebook": "https://www.facebook.com",
            "ফেসবুক": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "ইনস্টাগ্রাম": "https://www.instagram.com",
            "github": "https://www.github.com",
            "gmail": "https://mail.google.com",
            "জিমেইল": "https://mail.google.com",
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "ইউটিউব": "https://www.youtube.com",
            "whatsapp": "https://web.whatsapp.com",
            "হোয়াটসঅ্যাপ": "https://web.whatsapp.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com",
            "wikipedia": "https://www.wikipedia.org",
            "stackoverflow": "https://stackoverflow.com",
            "reddit": "https://www.reddit.com",
            "linkedin": "https://www.linkedin.com",
            "chatgpt": "https://chat.openai.com",
            "চ্যাটজিপিটি": "https://chat.openai.com",
        }
        url = sites.get(site.lower())
        if not url:
            if not site.startswith("http"):
                url = f"https://www.{site}.com"
            else:
                url = site
        webbrowser.open(url)
        self.assistant.speak(f"{site} খোলা হচ্ছে।")

    def _open_app_or_site(self, name: str) -> bool:
        """অ্যাপ অথবা ওয়েবসাইট খোলো।"""
        name_lower = name.lower().strip()

        # ── বিল্ট-ইন Windows অ্যাপ — সরাসরি subprocess ──
        builtin_apps = {
            "calculator": "calc.exe",
            "ক্যালকুলেটর": "calc.exe",
            "calc": "calc.exe",
            "notepad": "notepad.exe",
            "নোটপ্যাড": "notepad.exe",
            "paint": "mspaint.exe",
            "পেইন্ট": "mspaint.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "কমান্ড প্রম্পট": "cmd.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "ফাইল এক্সপ্লোরার": "explorer.exe",
            "wordpad": "wordpad.exe",
            "task manager": "taskmgr.exe",
            "টাস্ক ম্যানেজার": "taskmgr.exe",
            "registry": "regedit.exe",
        }
        for key, exe in builtin_apps.items():
            if key in name_lower:
                try:
                    subprocess.Popen([exe])
                    self.assistant.speak(f"{name} চালু হচ্ছে।")
                    return True
                except Exception:
                    try:
                        subprocess.Popen(exe, shell=True)
                        self.assistant.speak(f"{name} চালু হচ্ছে।")
                        return True
                    except Exception:
                        pass

        # ── ওয়েবসাইট চেক ──
        web_sites = [
            "youtube", "google", "facebook", "instagram", "twitter",
            "github", "gmail", "whatsapp", "netflix", "amazon",
            "wikipedia", "stackoverflow", "reddit", "linkedin", "chatgpt",
            "ইউটিউব", "ফেসবুক", "ইনস্টাগ্রাম", "জিমেইল",
        ]
        if name_lower in web_sites:
            self._open_website(name)
            return True

        # ── settings APPS dict ──
        apps = self.settings.APPS
        for app_name, app_path in apps.items():
            if name_lower in app_name.lower() or app_name.lower() in name_lower:
                try:
                    if "*" in app_path:
                        matches = glob.glob(app_path)
                        app_path = matches[0] if matches else app_path

                    expanded = os.path.expandvars(app_path)
                    if os.path.exists(expanded):
                        subprocess.Popen([expanded])
                    else:
                        subprocess.Popen(app_path, shell=True)
                    self.assistant.speak(f"{app_name} চালু হচ্ছে।")
                    return True
                except Exception:
                    self.assistant.speak(f"{app_name} খুলতে পারলাম না।")
                    return False

        # কোনো match না হলে Google সার্চ
        self._search_google(name)
        return True

    def _close_app(self, name: str) -> bool:
        """অ্যাপ বন্ধ করো।"""
        exe_map = {
            "chrome": "chrome.exe",
            "ক্রোম": "chrome.exe",
            "firefox": "firefox.exe",
            "notepad": "notepad.exe",
            "নোটপ্যাড": "notepad.exe",
            "calculator": "calc.exe",
            "ক্যালকুলেটর": "calc.exe",
            "vlc": "vlc.exe",
            "spotify": "Spotify.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "whatsapp": "WhatsApp.exe",
            "হোয়াটসঅ্যাপ": "WhatsApp.exe",
            "telegram": "Telegram.exe",
        }
        exe = None
        for key, val in exe_map.items():
            if key in name.lower():
                exe = val
                break

        if exe:
            os.system(f"taskkill /f /im {exe} >nul 2>&1")
            self.assistant.speak(f"{name} বন্ধ করা হয়েছে।")
        else:
            self.assistant.speak(f"{name} কীভাবে বন্ধ করবো বুঝতে পারলাম না।")
        return True

    # ══════════════════════════════════════════
    # 🖱️ মাউস কন্ট্রোল
    # ══════════════════════════════════════════

    def _mouse_move(self, dx: int, dy: int):
        if not HAS_PYAUTOGUI:
            self.assistant.speak("pyautogui ইনস্টল করো।"); return
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(x + dx, y + dy,
                             duration=self.settings.MOUSE_MOVE_SPEED)
            self.assistant.speak("মাউস সরানো হয়েছে।")
        except Exception as e:
            self.assistant.speak(f"মাউস সরাতে সমস্যা।")

    def _mouse_click(self):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.click()
            self.assistant.speak("ক্লিক করা হয়েছে।")
        except Exception:
            pass

    def _mouse_double_click(self):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.doubleClick()
            self.assistant.speak("ডাবল ক্লিক করা হয়েছে।")
        except Exception:
            pass

    def _mouse_right_click(self):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.rightClick()
            self.assistant.speak("রাইট ক্লিক করা হয়েছে।")
        except Exception:
            pass

    def _scroll(self, amount: int):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.scroll(amount)
            direction = "উপরে" if amount > 0 else "নিচে"
            self.assistant.speak(f"{direction} স্ক্রল করা হয়েছে।")
        except Exception:
            pass

    # ══════════════════════════════════════════
    # ⌨️ কীবোর্ড কন্ট্রোল
    # ══════════════════════════════════════════

    def _type_text(self, text: str):
        if not HAS_PYAUTOGUI:
            self.assistant.speak("pyautogui ইনস্টল করো।"); return
        try:
            pyautogui.write(text, interval=self.settings.TYPING_INTERVAL)
            self.assistant.speak(f"লেখা হয়েছে।")
        except Exception:
            self.assistant.speak("টাইপ করতে সমস্যা হচ্ছে।")

    def _press_key(self, key: str):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.press(key)
        except Exception:
            pass

    def _hotkey(self, *keys):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.hotkey(*keys)
        except Exception:
            pass

    # ══════════════════════════════════════════
    # 🪟 উইন্ডো কন্ট্রোল
    # ══════════════════════════════════════════

    def _window_minimize(self):
        self._hotkey("win", "down")
        self.assistant.speak("উইন্ডো মিনিমাইজ করা হয়েছে।")

    def _window_maximize(self):
        self._hotkey("win", "up")
        self.assistant.speak("উইন্ডো ম্যাক্সিমাইজ করা হয়েছে।")

    def _window_close(self):
        self._hotkey("alt", "f4")
        self.assistant.speak("উইন্ডো বন্ধ করা হয়েছে।")

    def _minimize_all(self):
        self._hotkey("win", "d")
        self.assistant.speak("সব উইন্ডো মিনিমাইজ — ডেস্কটপ দেখা যাচ্ছে।")

    def _alt_tab(self):
        if not HAS_PYAUTOGUI:
            return
        try:
            pyautogui.keyDown("alt")
            time.sleep(0.1)
            pyautogui.press("tab")
            time.sleep(0.5)
            pyautogui.keyUp("alt")
            self.assistant.speak("উইন্ডো পরিবর্তন করা হয়েছে।")
        except Exception:
            pass

    # ══════════════════════════════════════════
    # 🖥️ সিস্টেম কমান্ড
    # ══════════════════════════════════════════

    def _take_screenshot(self):
        try:
            if HAS_PYAUTOGUI:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                filename = os.path.join(desktop, f"screenshot_{timestamp}.png")
                screenshot = pyautogui.screenshot()
                screenshot.save(filename)
                self.assistant.speak(f"স্ক্রিনশট ডেস্কটপে সেভ হয়েছে।")
            else:
                # Windows snipping tool fallback
                subprocess.Popen(["snippingtool"], shell=True)
                self.assistant.speak("স্ক্রিনশট টুল চালু হয়েছে।")
        except Exception as e:
            self.assistant.speak("স্ক্রিনশট নিতে পারলাম না।")

    def _lock_screen(self):
        self.assistant.speak("স্ক্রিন লক হচ্ছে।")
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])

    def _shutdown(self):
        self.assistant.speak("১০ সেকেন্ড পরে কম্পিউটার বন্ধ হবে। বাতিল করতে বলো।")
        subprocess.Popen("shutdown /s /t 10", shell=True)

    def _restart(self):
        self.assistant.speak("১০ সেকেন্ড পরে রিস্টার্ট হবে।")
        subprocess.Popen("shutdown /r /t 10", shell=True)

    def _sleep(self):
        self.assistant.speak("কম্পিউটার ঘুমাচ্ছে। শুভ রাত্রি!")
        time.sleep(1)
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])

    def _empty_recycle_bin(self):
        subprocess.run(
            ["powershell", "-Command",
             "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
            capture_output=True
        )
        self.assistant.speak("রিসাইকেল বিন খালি করা হয়েছে।")

    # ══════════════════════════════════════════
    # 🔊 ভলিউম কন্ট্রোল
    # ══════════════════════════════════════════

    def _volume_change(self, direction: str):
        """Windows native keybd_event দিয়ে ভলিউম বদলাও।"""
        if HAS_CTYPES:
            key_code = 0xAF if direction == "up" else 0xAE
            for _ in range(5):
                ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
                ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)
                time.sleep(0.05)
            msg = "ভলিউম বাড়ানো হয়েছে।" if direction == "up" else "ভলিউম কমানো হয়েছে।"
            self.assistant.speak(msg)
        elif HAS_PYAUTOGUI:
            key = "volumeup" if direction == "up" else "volumedown"
            for _ in range(5):
                pyautogui.press(key)
            self.assistant.speak("ভলিউম পরিবর্তন হয়েছে।")
        else:
            self.assistant.speak("ভলিউম কন্ট্রোল সম্ভব হচ্ছে না।")

    def _mute(self):
        """Mute/Unmute toggle।"""
        if HAS_CTYPES:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
        elif HAS_PYAUTOGUI:
            pyautogui.press("volumemute")
        self.assistant.speak("মিউট করা হয়েছে।")

    def _set_volume(self, level: int):
        """নির্দিষ্ট ভলিউম সেট করো (0-100)।"""
        level = max(0, min(100, level))
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            self.assistant.speak(f"ভলিউম {level} শতাংশে সেট করা হয়েছে।")
        except Exception:
            self.assistant.speak(f"ভলিউম {level} এ সেট করতে পারলাম না।")

    # ══════════════════════════════════════════
    # 🎵 মিডিয়া কন্ট্রোল
    # ══════════════════════════════════════════

    def _media_play_pause(self):
        if HAS_CTYPES:
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
        elif HAS_PYAUTOGUI:
            pyautogui.press("playpause")

    def _media_next(self):
        if HAS_CTYPES:
            ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)
        elif HAS_PYAUTOGUI:
            pyautogui.press("nexttrack")
        self.assistant.speak("পরবর্তী ট্র্যাকে গেলাম।")

    def _media_previous(self):
        if HAS_CTYPES:
            ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)
        elif HAS_PYAUTOGUI:
            pyautogui.press("prevtrack")
        self.assistant.speak("আগের ট্র্যাকে গেলাম।")

    # ══════════════════════════════════════════
    # 💡 ব্রাইটনেস
    # ══════════════════════════════════════════

    def _brightness(self, direction: str):
        try:
            import wmi
            c = wmi.WMI(namespace="wmi")
            methods = c.WmiMonitorBrightnessMethods()[0]
            current = c.WmiMonitorBrightness()[0].CurrentBrightness
            new_b = min(100, current + 10) if direction == "up" else max(0, current - 10)
            methods.WmiSetBrightness(new_b, 0)
            self.assistant.speak(f"ব্রাইটনেস {new_b} শতাংশে সেট হয়েছে।")
        except Exception:
            self.assistant.speak("ব্রাইটনেস পরিবর্তন করতে পারলাম না।")

    # ══════════════════════════════════════════
    # 📁 ফাইল ও ফোল্ডার
    # ══════════════════════════════════════════

    def _open_folder(self, folder_name: str):
        home = os.path.expanduser("~")
        folders = {
            "downloads": os.path.join(home, "Downloads"),
            "documents": os.path.join(home, "Documents"),
            "desktop":   os.path.join(home, "Desktop"),
            "pictures":  os.path.join(home, "Pictures"),
            "music":     os.path.join(home, "Music"),
            "videos":    os.path.join(home, "Videos"),
        }
        path = folders.get(folder_name.lower(), home)
        try:
            subprocess.Popen(f'explorer "{path}"')
            self.assistant.speak(f"{folder_name} ফোল্ডার খোলা হচ্ছে।")
        except Exception:
            self.assistant.speak(f"ফোল্ডার খুলতে পারলাম না।")

    # ══════════════════════════════════════════
    # 🧮 ক্যালকুলেশন (নিরাপদ)
    # ══════════════════════════════════════════

    def _calculate(self, command: str) -> bool:
        """নিরাপদ গাণিতিক হিসাব — eval() ছাড়া।"""
        try:
            expr = command
            for keyword in ["হিসাব করো", "calculate", "compute", "কত হয়", "what is",
                            "what's", "math"]:
                expr = expr.replace(keyword, "")

            # শব্দকে অপারেটরে রূপান্তর
            replacements = {
                "plus": "+", "যোগ": "+",
                "minus": "-", "বিয়োগ": "-",
                "times": "*", "গুণ": "*", "multiplied by": "*",
                "divided by": "/", "ভাগ": "/",
                "to the power of": "**", "squared": "**2",
            }
            for word, op in replacements.items():
                expr = expr.replace(word, op)

            expr = expr.strip()

            # শুধু নিরাপদ mathematical characters
            if not re.match(r'^[\d\s\+\-\*\/\(\)\.\,\*\*]+$', expr):
                return False

            # ast.literal_eval নয়, নিরাপদ math parser
            result = self._safe_eval(expr)
            if result is not None:
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.assistant.speak(f"উত্তর হলো {result}।")
                return True
        except Exception:
            pass
        return False

    def _safe_eval(self, expr: str):
        """নিরাপদ mathematical expression evaluator।"""
        # শুধু সংখ্যা ও অপারেটর অনুমতি
        allowed_chars = set("0123456789 +-*/().,**")
        if not all(c in allowed_chars for c in expr):
            return None
        try:
            # ast দিয়ে parse করো
            tree = ast.parse(expr, mode='eval')
            return self._eval_node(tree.body)
        except Exception:
            return None

    def _eval_node(self, node):
        """AST node evaluate করো।"""
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = ops.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported op: {node.op}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = ops.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported op: {node.op}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported node: {node}")

    # ══════════════════════════════════════════
    # 💻 সিস্টেম তথ্য
    # ══════════════════════════════════════════

    def _system_info(self):
        import socket
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.assistant.speak(
                f"আপনার কম্পিউটারের নাম {hostname} এবং লোকাল আইপি হলো {ip}।"
            )
        except Exception:
            self.assistant.speak("সিস্টেম তথ্য পেলাম না।")

    def _battery_info(self):
        try:
            import psutil
            b = psutil.sensors_battery()
            if b:
                status = "চার্জ হচ্ছে" if b.power_plugged else "ব্যাটারিতে চলছে"
                self.assistant.speak(
                    f"ব্যাটারি চার্জ {int(b.percent)} শতাংশ এবং {status}।"
                )
            else:
                self.assistant.speak("ডেস্কটপ পিসি — ব্যাটারি নেই, সরাসরি বিদ্যুতে চলছে।")
        except ImportError:
            self.assistant.speak("psutil ইনস্টল করো: pip install psutil")

    def _ram_info(self):
        try:
            import psutil
            mem = psutil.virtual_memory()
            used_gb = round(mem.used / (1024 ** 3), 1)
            total_gb = round(mem.total / (1024 ** 3), 1)
            self.assistant.speak(
                f"র‍্যাম ব্যবহার হচ্ছে {used_gb} গিগাবাইট, মোট আছে {total_gb} গিগাবাইট।"
            )
        except ImportError:
            self.assistant.speak("psutil ইনস্টল করো।")

    def _cpu_info(self):
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=1)
            self.assistant.speak(f"CPU ব্যবহার {cpu} শতাংশ।")
        except ImportError:
            self.assistant.speak("psutil ইনস্টল করো।")

    def _disk_info(self):
        try:
            import psutil
            disk = psutil.disk_usage("C:\\")
            free_gb = round(disk.free / (1024 ** 3), 1)
            total_gb = round(disk.total / (1024 ** 3), 1)
            self.assistant.speak(
                f"C ড্রাইভে মোট {total_gb} গিগাবাইট, ফাঁকা আছে {free_gb} গিগাবাইট।"
            )
        except ImportError:
            self.assistant.speak("psutil ইনস্টল করো।")

    # ══════════════════════════════════════════
    # 🎉 মজার কমান্ড
    # ══════════════════════════════════════════

    def _tell_joke(self):
        jokes = [
            "প্রোগ্রামার কাঁদছে কেন? কারণ সে loop থেকে বের হতে পারছে না!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "কম্পিউটার ঠান্ডা কেন? কারণ Windows খোলা আছে!",
            "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
            "Why did the programmer quit? He didn't get arrays!",
            "ডেভেলপার মারা গেলে কোথায় যায়? localhost-এ!",
        ]
        self.assistant.speak(random.choice(jokes))

    def _flip_coin(self):
        result = random.choice(["মাথা (Heads)", "পেট (Tails)"])
        self.assistant.speak(f"কয়েন ফেললাম — {result}!")

    def _roll_dice(self):
        result = random.randint(1, 6)
        self.assistant.speak(f"ডাইস ছুঁড়লাম — {result} উঠেছে!")

    def _random_number(self):
        result = random.randint(1, 100)
        self.assistant.speak(f"র‍্যান্ডম নম্বর হলো {result}।")

    # ══════════════════════════════════════════
    # 🔧 ইউটিলিটি
    # ══════════════════════════════════════════

    def _clear_history(self):
        if hasattr(self.assistant, 'conversation_history'):
            self.assistant.conversation_history.clear()
        self.assistant.speak("কথোপকথনের ইতিহাস মুছে ফেলা হয়েছে। নতুন করে শুরু করছি!")

    def _m(self, command: str, patterns: list) -> bool:
        """কমান্ড যেকোনো প্যাটার্নের সাথে মিলছে কিনা চেক করো।"""
        return any(pattern in command for pattern in patterns)
