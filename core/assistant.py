"""
JARVIS Core Assistant Engine — Full Hands-Free Voice PC Control
শুধু কথা বললেই কম্পিউটারের সব কাজ হবে।
"""

import os
import re
import sys
import time
import random
import datetime
import threading
import subprocess
import platform

from core.speech import SpeechEngine
from core.ai_brain import AIBrain
from core.commands import CommandProcessor
from core.display import Display
from core.universal_agent import UniversalAgent


class JarvisAssistant:
    """JARVIS এর মূল ক্লাস — Hands-Free Voice PC Control।"""

    def __init__(self, settings, display: Display):
        self.settings = settings
        self.display = display
        self.is_running = False
        self.conversation_history = []
        self._voice_thread = None

        print("\033[93m  [*] Speech Engine লোড হচ্ছে...\033[0m")
        self.speech = SpeechEngine(settings)

        print("\033[93m  [*] AI Brain সংযুক্ত হচ্ছে...\033[0m")
        self.ai = AIBrain(settings)

        print("\033[93m  [*] Command Processor প্রস্তুত হচ্ছে...\033[0m")
        self.commands = CommandProcessor(settings, self)

        print("\033[93m  [*] Universal Agent (AI PC Controller) লোড হচ্ছে...\033[0m")
        self.agent = UniversalAgent(settings, ai_brain=self.ai, speech_engine=self.speech)

        self.greetings = [
            "অনলাইন। কী করতে পারি বলুন।",
            "জারভিস সক্রিয়। আপনার সেবায় প্রস্তুত।",
            "সিস্টেম সম্পূর্ণ প্রস্তুত। বলুন কী দরকার।",
            "হ্যাঁ স্যার, শুনছি।",
        ]
        self.farewells = [
            "বিদায়! ভালো থাকবেন।",
            "জারভিস বন্ধ হচ্ছে। পরে দেখা হবে।",
            "ঠিক আছে, বিদায়! আবার ডাকলেই আসব।",
            "শাটডাউন করছি। পরে কথা হবে।",
        ]
        self.not_understood = [
            "দুঃখিত, বুঝতে পারলাম না। আবার বলবেন?",
            "ক্ষমা করবেন, আবার একটু বলুন।",
            "সঠিকভাবে বুঝতে পারিনি। আরেকবার বলুন।",
        ]

    def speak(self, text: str):
        """JARVIS কথা বলবে এবং terminal এ দেখাবে।"""
        self.display.jarvis_response(text)
        self.speech.speak(text)

    def listen(self) -> str:
        """মাইক্রোফোন থেকে কথা শুনবে।"""
        self.display.listening_indicator()
        text = self.speech.listen()
        if text:
            self.display.user_input(text)
        return text or ""

    def process_command(self, user_input: str) -> bool:
        """
        কমান্ড প্রসেস করে।
        Returns False যদি JARVIS বন্ধ করতে হয়।
        """
        if not user_input or not user_input.strip():
            return True

        user_input = user_input.strip()
        cmd = user_input.lower()

        # ── বন্ধ করার কমান্ড ────────────────────
        exit_phrases = [
            "goodbye jarvis", "bye jarvis", "exit", "quit",
            "বিদায় জারভিস", "বন্ধ হও", "বন্ধ হয়ে যাও",
            "ঘুমাও", "বিদায়", "শেষ করো",
        ]
        if any(phrase in cmd for phrase in exit_phrases):
            self.speak(random.choice(self.farewells))
            return False

        # শাটডাউন শব্দ (কিন্তু shutdown PC নয়, JARVIS বন্ধ করা)
        if cmd in ["shutdown jarvis", "stop jarvis", "close jarvis"]:
            self.speak(random.choice(self.farewells))
            return False

        # ── সাহায্য কমান্ড ───────────────────────
        if cmd in ["help", "সাহায্য", "কমান্ড", "কী করতে পারো", "what can you do"]:
            self.show_help()
            return True

        # ── সিস্টেম কমান্ড চেক ─────────────────
        handled = self.commands.process(user_input)
        if handled:
            return True

        # ── Universal Agent দিয়ে চেষ্টা করো (AI-powered PC control) ──
        self.display.thinking_indicator()
        result = self.agent.execute(user_input)

        if result and result.get("success"):
            reply = result.get("reply", "কাজটি করা হয়েছে।")
            self.speak(reply)
            # conversation history update
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})
            return True

        # ── Universal Agent handle করতে না পারলে AI Brain কে জিজ্ঞেস করো ──
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        recent_history = self.conversation_history[-self.settings.MAX_HISTORY:]
        response = self.ai.get_response(user_input, recent_history)

        if response:
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            self.speak(response)
        else:
            self.speak(random.choice(self.not_understood))

        return True

    def show_help(self):
        """উপলব্ধ কমান্ডের তালিকা দেখাও।"""
        help_text = """
╔══════════════════════════════════════════════════════════╗
║              🤖 JARVIS ভয়েস কমান্ড তালিকা               ║
╠══════════════════════════════════════════════════════════╣
║  🌐 ওয়েব:                                               ║
║    "গুগলে সার্চ করো [বিষয়]"  "ইউটিউবে [গান]"          ║
║    "ফেসবুক খোলো"  "জিমেইল খোলো"                        ║
║                                                          ║
║  🖥️ অ্যাপ:                                               ║
║    "নোটপ্যাড খোলো"  "ক্যালকুলেটর খোলো"                 ║
║    "ক্রোম খোলো"  "[অ্যাপ] বন্ধ করো"                    ║
║                                                          ║
║  🖱️ মাউস ও কীবোর্ড:                                      ║
║    "মাউস উপরে/নিচে/বামে/ডানে"  "ক্লিক করো"             ║
║    "টাইপ করো [লেখা]"  "কপি করো"  "পেস্ট করো"           ║
║    "স্ক্রল আপ/ডাউন"  "উইন্ডো বন্ধ"                      ║
║                                                          ║
║  🔊 ভলিউম ও মিডিয়া:                                     ║
║    "ভলিউম বাড়াও/কমাও"  "মিউট করো"  "ভলিউম ৫০"         ║
║    "পরবর্তী গান"  "আগের গান"  "গান বাজাও/থামাও"         ║
║                                                          ║
║  💻 সিস্টেম:                                             ║
║    "স্ক্রিনশট নাও"  "স্ক্রিন লক"  "শাটডাউন"            ║
║    "ব্যাটারি"  "র‍্যাম"  "সিপিইউ"  "ডিস্ক স্পেস"         ║
║    "সব মিনিমাইজ"  "টাস্ক ম্যানেজার"                     ║
║                                                          ║
║  📅 তথ্য:                                                ║
║    "সময় কত"  "আজ কত তারিখ"  "কি বার"                   ║
║                                                          ║
║  🎉 মজা:                                                 ║
║    "জোকস বলো"  "কয়েন ফ্লিপ"  "র‍্যান্ডম নম্বর"          ║
║                                                          ║
║  🛑 নিয়ন্ত্রণ:                                           ║
║    "বিদায় জারভিস"  "ইতিহাস মুছো"                        ║
╚══════════════════════════════════════════════════════════╝
        """
        print("\033[96m" + help_text + "\033[0m")
        self.speak("কমান্ড তালিকা স্ক্রিনে দেখা যাচ্ছে।")

    def greet(self):
        """শুরুতে অভিবাদন করো।"""
        hour = datetime.datetime.now().hour

        if 5 <= hour < 12:
            time_greeting = "শুভ সকাল"
        elif 12 <= hour < 17:
            time_greeting = "শুভ দুপুর"
        elif 17 <= hour < 21:
            time_greeting = "শুভ সন্ধ্যা"
        else:
            time_greeting = "শুভ রাত্রি"

        greeting = f"{time_greeting}! {random.choice(self.greetings)}"
        self.speak(greeting)

    def run(self):
        """JARVIS এর মূল লুপ — Hands-Free Mode।"""
        self.is_running = True
        self.greet()

        print("\n\033[90m" + "─" * 60 + "\033[0m")
        print("\033[94m[i] ভয়েসে বলুন অথবা টাইপ করুন। 'help' লিখলে কমান্ড দেখবেন।\033[0m\n")

        while self.is_running:
            try:
                user_input = self._get_input_smart()

                if not user_input:
                    continue

                should_continue = self.process_command(user_input)
                if not should_continue:
                    self.is_running = False
                    break

            except KeyboardInterrupt:
                self.speak("ঠিক আছে, বিদায়! জারভিস বন্ধ হচ্ছে।")
                self.is_running = False
                break
            except Exception as e:
                print(f"\033[91m[Error] {e}\033[0m")
                continue

    def _get_input_smart(self) -> str:
        """
        Smart Input: Voice + Typing একসাথে।
        যে আগে input দেবে সেটা নেওয়া হবে।
        """
        result = [None]
        input_ready = threading.Event()

        def _keyboard_thread():
            try:
                print("\n\033[94m┌─[JARVIS]─> \033[0m", end="", flush=True)
                text = input("")
                if not input_ready.is_set() and text.strip():
                    result[0] = text.strip()
                    input_ready.set()
            except (EOFError, KeyboardInterrupt):
                result[0] = "quit"
                input_ready.set()

        def _voice_thread():
            try:
                if self.speech.microphone and self.speech.recognizer:
                    text = self.listen()
                    if text and not input_ready.is_set():
                        result[0] = text
                        input_ready.set()
            except Exception:
                pass

        # দুটো thread একসাথে চালু করো
        kt = threading.Thread(target=_keyboard_thread, daemon=True)
        vt = threading.Thread(target=_voice_thread, daemon=True)
        kt.start()

        # শুধু মাইক থাকলে voice thread চালু করো
        if self.speech.microphone:
            vt.start()

        # যেকোনো একটি input আসার জন্য অপেক্ষা করো
        input_ready.wait(timeout=30)
        return result[0] or ""

    def _get_input(self) -> str:
        """শুধু কীবোর্ড থেকে ইনপুট।"""
        try:
            user_input = input("")
            return user_input.strip() if user_input.strip() else None
        except (EOFError, KeyboardInterrupt):
            return "quit"
