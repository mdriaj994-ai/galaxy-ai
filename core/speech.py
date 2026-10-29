"""
JARVIS Speech Engine
কথা শোনা (STT) এবং কথা বলা (TTS) পরিচালনা করে।
"""

import os
import io
import sys
import time
import random
import threading
import tempfile
import subprocess

# Windows UTF-8 Terminal Fix
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


class SpeechEngine:
    """Speech-to-Text এবং Text-to-Speech ইঞ্জিন।"""

    def __init__(self, settings):
        self.settings = settings
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        self._tts_lock = threading.Lock()

        self._init_tts()
        self._init_stt()

    # ══════════════════════════════════════════
    # 🔊 Text-to-Speech (কথা বলা)
    # ══════════════════════════════════════════

    def _init_tts(self):
        """TTS ইঞ্জিন শুরু করো।"""
        if self.settings.TTS_ENGINE == "cartesia":
            print("\033[92m  [✓] Cartesia AI Voice Engine সক্রিয় (My Zentic Voice)\033[0m")
        elif self.settings.TTS_ENGINE == "edge-tts":
            try:
                import edge_tts
                import pygame
                print("\033[92m  [✓] Microsoft Edge Neural TTS Engine সক্রিয় (বাস্তব পুরুষ কণ্ঠ)\033[0m")
            except Exception as e:
                print(f"\033[93m[!] Edge TTS লোড ত্রুটি: {e}\033[0m")
        elif self.settings.TTS_ENGINE == "pyttsx3":
            self._init_pyttsx3()
        elif self.settings.TTS_ENGINE == "gtts":
            self._check_gtts()

    def speak(self, text: str):
        """টেক্সট পড়ে শোনাও।"""
        if not text:
            return
        text = self._clean_text(text)
        with self._tts_lock:
            if self.settings.TTS_ENGINE == "cartesia":
                self._speak_cartesia(text)
            elif self.settings.TTS_ENGINE == "edge-tts":
                self._speak_edge_tts(text)
            elif self.settings.TTS_ENGINE == "pyttsx3" and self.tts_engine:
                self._speak_pyttsx3(text)
            elif self.settings.TTS_ENGINE == "gtts":
                self._speak_gtts(text)

    def _speak_cartesia(self, text: str):
        """Cartesia AI Ultra-realistic Voice দিয়ে সরাসরি মানুষের মতো কণ্ঠে কথা বলা।"""
        try:
            import requests
            import pygame
            import tempfile

            api_key = getattr(self.settings, 'CARTESIA_API_KEY', '') or os.getenv('CARTESIA_API_KEY', '')
            voice_id = getattr(self.settings, 'CARTESIA_VOICE_ID', '') or os.getenv('CARTESIA_VOICE_ID', '09ff9493-419d-45fc-937d-411115824bfc')
            model_id = getattr(self.settings, 'CARTESIA_MODEL', 'sonic-3.6')

            if not api_key:
                self._speak_edge_tts(text)
                return

            resp = requests.post(
                'https://api.cartesia.ai/tts/bytes',
                headers={
                    'Cartesia-Version': '2024-06-10',
                    'X-API-Key': api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'model_id': model_id,
                    'transcript': text,
                    'voice': {'mode': 'id', 'id': voice_id},
                    'output_format': {'container': 'mp3', 'encoding': 'mp3', 'sample_rate': 44100},
                    'language': 'bn'
                },
                timeout=12
            )

            if resp.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                    tmp_p = tmp.name
                    tmp.write(resp.content)

                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
                pygame.mixer.music.load(tmp_p)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
                pygame.mixer.music.stop()
                try:
                    os.unlink(tmp_p)
                except Exception:
                    pass
            else:
                print(f"[Cartesia Error {resp.status_code}, falling back to Edge TTS]: {resp.text[:100]}", flush=True)
                self._speak_edge_tts(text)
        except Exception as e:
            print(f"[Cartesia Exception, falling back to Edge TTS]: {e}", flush=True)
            self._speak_edge_tts(text)

    def _speak_edge_tts(self, text: str):
        """Microsoft Edge Neural Voice দিয়ে বাস্তবসম্মত পুরুষ কণ্ঠে স্পষ্ট বাংলায় কথা বলো।"""
        try:
            import asyncio
            import edge_tts
            import pygame
            import tempfile

            # Detect language
            ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(len(text), 1)
            if ascii_ratio > 0.8:
                voice = getattr(self.settings, 'EDGE_TTS_VOICE_EN', 'en-US-ChristopherNeural')
            else:
                voice = 'bn-IN-BashkarNeural'  # সবচেয়ে বাস্তবসম্মত বাংলা পুরুষ কণ্ঠ (hardcoded)

            async def _gen():
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                    tmp_p = tmp.name
                comm = edge_tts.Communicate(text, voice, rate='+5%', pitch='+0Hz')
                await comm.save(tmp_p)
                return tmp_p

            tmp_path = asyncio.run(_gen())

            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
            pygame.mixer.music.stop()
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
        except Exception as e:
            print(f"[Edge TTS Error, falling back to gTTS]: {e}", flush=True)
            self._speak_gtts(text)

    def _init_pyttsx3(self):
        """pyttsx3 শুরু করো।"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', self.settings.TTS_RATE)
            self.tts_engine.setProperty('volume', self.settings.TTS_VOLUME)
            voices = self.tts_engine.getProperty('voices')
            if voices:
                if self.settings.TTS_VOICE_GENDER == "female" and len(voices) > 1:
                    self.tts_engine.setProperty('voice', voices[1].id)
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            print("\033[92m  [✓] pyttsx3 TTS Engine সক্রিয়\033[0m")
        except ImportError:
            print("\033[91m[!] pyttsx3 ইনস্টল করুন: pip install pyttsx3\033[0m")
            self.tts_engine = None
        except Exception as e:
            print(f"\033[91m[!] TTS সমস্যা: {e}\033[0m")
            self.tts_engine = None

    def _check_gtts(self):
        """gTTS পরীক্ষা করো।"""
        try:
            import gtts
            import pygame
            print("\033[92m  [✓] gTTS + pygame Engine সক্রিয়\033[0m")
        except ImportError as e:
            missing = str(e).split("'")[-2] if "'" in str(e) else str(e)
            print(f"\033[91m[!] gTTS সেটআপ অসম্পূর্ণ: pip install gtts pygame\033[0m")

    def speak(self, text: str):
        """টেক্সট পড়ে শোনাও।"""
        if not text:
            return
        text = self._clean_text(text)
        with self._tts_lock:
            if self.settings.TTS_ENGINE == "pyttsx3" and self.tts_engine:
                self._speak_pyttsx3(text)
            elif self.settings.TTS_ENGINE == "gtts":
                self._speak_gtts(text)

    def _speak_pyttsx3(self, text: str):
        """pyttsx3 দিয়ে কথা বলো।"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except RuntimeError:
            try:
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.settings.TTS_RATE)
                self.tts_engine.setProperty('volume', self.settings.TTS_VOLUME)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception:
                pass
        except Exception as e:
            print(f"\033[91m[TTS Error] {e}\033[0m")

    def _speak_gtts(self, text: str):
        """gTTS দিয়ে বাংলা/ইংরেজি কথা বলো — PC স্পিকারে শোনাবে।"""
        tmp_path = None
        try:
            from gtts import gTTS

            # বাংলা vs ইংরেজি detect করো
            lang = self.settings.GTTS_LANG
            if lang == "bn":
                # যদি বেশিরভাগ ASCII (ইংরেজি) হয়, তাহলে en ব্যবহার করো
                ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(len(text), 1)
                if ascii_ratio > 0.8:
                    lang = "en"

            tts = gTTS(text=text, lang=lang, slow=False)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tmp_path = tmp.name
                tts.save(tmp_path)

            played = False

            # পদ্ধতি ১: pygame
            try:
                import pygame
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
                pygame.mixer.music.stop()
                played = True
            except Exception as pg_err:
                print(f"[gTTS pygame]: {pg_err}", flush=True)

            # পদ্ধতি ২: playsound
            if not played:
                try:
                    from playsound import playsound
                    playsound(tmp_path, block=True)
                    played = True
                except Exception as ps_err:
                    print(f"[gTTS playsound]: {ps_err}", flush=True)

            # পদ্ধতি ৩: Windows built-in — VLC বা wmplayer (mp3 সাপোর্ট)
            if not played:
                try:
                    # vlc commandline
                    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
                    if os.path.exists(vlc_path):
                        subprocess.run(
                            [vlc_path, "--intf", "dummy", "--play-and-exit", tmp_path],
                            timeout=30, capture_output=True
                        )
                        played = True
                except Exception:
                    pass

            # পদ্ধতি ৪: Windows Media Player via PowerShell (সঠিক COM object)
            if not played:
                try:
                    ps_cmd = (
                        f"$player = New-Object System.Windows.Media.MediaPlayer; "
                        f"$player.Open([uri]::new('{tmp_path}')); "
                        f"$player.Play(); Start-Sleep -Seconds 10"
                    )
                    subprocess.run(
                        ["powershell", "-Command", ps_cmd],
                        timeout=15, capture_output=True
                    )
                except Exception:
                    pass

        except ImportError:
            print("\033[91m[!] gtts ইনস্টল করো: pip install gtts pygame\033[0m")
        except Exception as e:
            print(f"[gTTS Error]: {e}", flush=True)
        finally:
            # অস্থায়ী ফাইল মুছো
            if tmp_path:
                try:
                    time.sleep(0.3)
                    os.unlink(tmp_path)
                except Exception:
                    pass

    def _clean_text(self, text: str) -> str:
        """TTS এর জন্য টেক্সট পরিষ্কার করো।"""
        import re
        # ইমোজি ও স্পেশাল সিম্বল বাদ দাও যাতে টিটিএস ক্লিয়ারলি উচ্চারণ করে
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        text = re.sub(r'[\u2600-\u27bf\u2300-\u23ff\ufe0f]', '', text)
        # মার্কডাউন সরাও
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'`+', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
        # একাধিক স্পেস সরাও
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # ══════════════════════════════════════════
    # 🎤 Speech-to-Text (কথা শোনা)
    # ══════════════════════════════════════════

    def _init_stt(self):
        """STT ইঞ্জিন শুরু করো।"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = self.settings.MIC_ENERGY_THRESHOLD
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8

            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("\033[92m  [✓] মাইক্রোফোন সংযুক্ত ও calibrate হয়েছে (PyAudio)\033[0m")
            except Exception:
                try:
                    import sounddevice as sd
                    self.has_sounddevice = True
                    self.microphone = None
                    print("\033[92m  [✓] মাইক্রোফোন সংযুক্ত হয়েছে (SoundDevice Engine)\033[0m")
                except Exception:
                    self.has_sounddevice = False
                    self.microphone = None
                    print("\033[93m  [!] মাইক্রোফোন পাওয়া যায়নি। Typing Mode ব্যবহার করুন।\033[0m")

        except ImportError:
            print("\033[91m[!] speech_recognition ইনস্টল করুন: pip install SpeechRecognition\033[0m")
            self.recognizer = None

    def listen(self) -> str:
        """মাইক্রোফোন থেকে কথা শোনো (PyAudio অথবা SoundDevice দিয়ে)।"""
        if not self.recognizer:
            return ""

        # SoundDevice ফলব্যাক
        if getattr(self, 'has_sounddevice', False) and not self.microphone:
            return self._listen_sounddevice()

        if not self.microphone:
            return ""

        try:
            import speech_recognition as sr
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                print("\033[94m  🎤 শুনছি...\033[0m", end="\r", flush=True)
                audio = self.recognizer.listen(
                    source,
                    timeout=self.settings.MIC_TIMEOUT,
                    phrase_time_limit=self.settings.MIC_PHRASE_TIMEOUT
                )
                print("\033[93m  🔄 বুঝছি...\033[0m", end="\r", flush=True)

            text = self.recognizer.recognize_google(
                audio,
                language=self.settings.LANGUAGE
            )
            return text

        except Exception as e:
            return ""

    def _listen_sounddevice(self) -> str:
        """PyAudio ছাড়া সরাসরি sounddevice দিয়ে রেকর্ড ও রিকগনিশন।"""
        try:
            import sounddevice as sd
            import speech_recognition as sr
            import numpy as np

            fs = 16000
            duration = min(self.settings.MIC_TIMEOUT or 6, 8)
            print("\033[94m  🎤 শুনছি (কথা বলুন)...\033[0m", end="\r", flush=True)

            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()

            # শব্দ থাকলে গুগল রিকগনিশনে পাঠাও
            if np.max(np.abs(recording)) < 400:
                return ""

            print("\033[93m  🔄 বুঝছি...\033[0m", end="\r", flush=True)
            audio_bytes = recording.tobytes()
            audio_data = sr.AudioData(audio_bytes, fs, 2)
            text = self.recognizer.recognize_google(
                audio_data,
                language=self.settings.LANGUAGE
            )
            return text.strip()
        except Exception:
            return ""

    def listen_for_wake_word(self) -> bool:
        """ওয়েক ওয়ার্ড শোনার চেষ্টা করো।"""
        text = self.listen()
        if text:
            text_lower = text.lower()
            return any(phrase in text_lower for phrase in self.settings.WAKE_PHRASES)
        return False
