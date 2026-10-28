"""
JARVIS Web Dashboard Server
বাংলা ভয়েস রিকগনিশন ও পিসি অটোমেশন সার্ভার
"""

import os
import sys
import threading
import webbrowser
import time
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

# Windows Terminal UTF-8 Encoding Fix
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Ensure project root in path
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from config.settings import Settings
from core.ai_brain import AIBrain
from core.speech import SpeechEngine
from core.universal_agent import UniversalAgent

app = Flask(__name__, static_folder="web")
CORS(app)

# Initialize Core Services
print("\033[96m[*] Initializing JARVIS Universal Engine...\033[0m")
settings = Settings()
speech_engine = SpeechEngine(settings)
ai_brain = AIBrain(settings)
agent = UniversalAgent(settings, ai_brain=ai_brain, speech_engine=speech_engine)

print("\033[92m[✓] Universal Agent is ready! Photoshop path:\033[0m", agent.photoshop_path)


# ──────────────────────────────────────────
# 🌐 Web Routes
# ──────────────────────────────────────────

@app.route("/")
def index():
    """ড্যাশবোর্ডের মূল পেজ রিটার্ন করে।"""
    return send_from_directory("web", "index.html")


@app.route("/<path:path>")
def static_files(path):
    """CSS, JS এবং অন্যান্য ফাইল পরিবেশন করে।"""
    return send_from_directory("web", path)


@app.route("/api/status", methods=["GET"])
def get_status():
    """সিস্টেম স্ট্যাটাস রিটার্ন করে।"""
    return jsonify({
        "status": "online",
        "gemini_model": settings.GEMINI_MODEL,
        "photoshop": agent.photoshop_path,
        "tts_engine": settings.TTS_ENGINE
    })


@app.route("/api/tts", methods=["GET"])
def tts_stream():
    """রিয়েলটাইম বাংলা অডিও তৈরি করে ব্রাউজারে শোনায় (gTTS)।"""
    text = request.args.get("text", "").strip()
    if not text:
        return "No text", 400
    try:
        from gtts import gTTS
        import io
        from flask import send_file
        fp = io.BytesIO()
        tts = gTTS(text=text, lang="bn", slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        return send_file(fp, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/command", methods=["POST"])
def execute_command():
    """
    ব্যবহারকারীর বাংলা বা ইংরেজি ভয়েস কমান্ড রিসিভ করে
    এবং কম্পিউটারে এক্সিকিউট করে।
    """
    data = request.get_json(silent=True) or {}
    user_cmd = data.get("command", "").strip()

    if not user_cmd:
        return jsonify({
            "success": False,
            "reply": "কোনো নির্দেশ পাওয়া যায়নি।",
            "details": "Empty command"
        }), 400

    print(f"\n\033[94m[Voice/Text Command]:\033[0m {user_cmd}", flush=True)

    # Universal Agent দিয়ে এক্সিকিউশন
    result = agent.execute(user_cmd)
    reply_text = result.get("reply", "")

    # ব্যাকগ্রাউন্ড থ্রেডে পিসির স্পিকার দিয়ে কথা বলা
    def safe_speak(text):
        try:
            speech_engine.speak(text)
        except Exception as e:
            print(f"[TTS Error]: {e}", flush=True)

    speak_pc = data.get("speak_pc", True)
    if reply_text and speak_pc:
        threading.Thread(target=safe_speak, args=(reply_text,), daemon=True).start()

    print(f"\033[92m[JARVIS Action]:\033[0m {result.get('action')} - {result.get('details')}", flush=True)
    print(f"\033[96m[JARVIS Reply]:\033[0m {reply_text}\n", flush=True)

    return jsonify(result)


@app.route("/api/voice_upload", methods=["POST"])
def voice_upload():
    """
    ব্রাউজারের MediaRecorder থেকে রেকর্ড করা অডিও রিসিভ করে,
    Google STT দিয়ে বাংলায় টেক্সট রূপান্তর করে এবং কমান্ড এক্সিকিউট করে।
    এটি AdsPower, Chrome, Edge সহ যেকোনো ব্রাউজারে ১০০% কাজ করে।
    """
    if "audio" not in request.files and not request.data:
        return jsonify({"success": False, "reply": "কোনো অডিও পাওয়া যায়নি।"}), 400

    lang = request.args.get("lang", "bn-BD")
    tmp_in = None
    tmp_out = None
    try:
        import tempfile
        import speech_recognition as sr
        import subprocess

        tmp_in = tempfile.mktemp(suffix=".webm")
        tmp_out = tempfile.mktemp(suffix=".wav")

        if "audio" in request.files:
            file = request.files["audio"]
            file.save(tmp_in)
        else:
            with open(tmp_in, "wb") as f:
                f.write(request.data)

        # FFmpeg দিয়ে 16kHz Mono WAV এ রূপান্তর
        subprocess.run(
            ["ffmpeg", "-y", "-i", tmp_in, "-ar", "16000", "-ac", "1", tmp_out],
            capture_output=True, timeout=10
        )

        recognizer = getattr(speech_engine, "recognizer", None) or sr.Recognizer()
        with sr.AudioFile(tmp_out) as source:
            audio_data = recognizer.record(source)

        try:
            transcript = recognizer.recognize_google(audio_data, language=lang).strip()
        except Exception:
            try:
                transcript = recognizer.recognize_google(audio_data, language="en-US").strip()
            except Exception:
                return jsonify({
                    "success": False,
                    "reply": "আপনার কথা স্পষ্ট শোনা যায়নি। অনুগ্রহ করে আবার বলুন।",
                    "details": "Speech not recognized"
                })

        print(f"\n\033[92m[Browser Voice Transcribed]:\033[0m {transcript}", flush=True)

        # কমান্ড এক্সিকিউট করো
        result = agent.execute(transcript)
        result["transcript"] = transcript
        return jsonify(result)

    except Exception as e:
        print(f"[Voice Upload Error]: {e}", flush=True)
        return jsonify({"success": False, "reply": f"ভয়েস প্রসেসিং এরর: {e}"}), 500
    finally:
        for p in [tmp_in, tmp_out]:
            if p and os.path.exists(p):
                try:
                    os.unlink(p)
                except Exception:
                    pass


@app.route("/api/tts")
def api_tts():
    """
    Microsoft Edge Neural Speech (PradeepNeural) দিয়ে বাস্তবসম্মত পুরুষ কণ্ঠের
    হাই-কোয়ালিটি MP3 অডিও তৈরি করে। এটি মোবাইল ও ব্রাউজারে পরিষ্কার শোনাবে।
    """
    text = request.args.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        import io
        import asyncio
        import edge_tts

        ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(len(text), 1)
        voice = getattr(settings, 'EDGE_TTS_VOICE_EN', 'en-US-ChristopherNeural') if ascii_ratio > 0.8 else getattr(settings, 'EDGE_TTS_VOICE_MALE', 'bn-BD-PradeepNeural')

        async def _gen():
            comm = edge_tts.Communicate(text, voice)
            data = b""
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    data += chunk["data"]
            return data

        audio_bytes = asyncio.run(_gen())
        return send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="reply.mp3"
        )
    except Exception as e:
        print(f"[API TTS Error]: {e}", flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/listen_mic", methods=["POST"])
def listen_hardware_mic():
    """
    পিসির ইউএসবি মাইক্রোফোন থেকে সরাসরি কথা শুনে এক্সিকিউট করে।
    """
    text = speech_engine.listen()
    if not text:
        return jsonify({
            "success": False,
            "reply": "মাইক্রোফোন থেকে কোনো কথা শোনা যায়নি। আবার চেষ্টা করুন।"
        })
    print(f"\n\033[92m[Hardware Mic Transcribed]:\033[0m {text}", flush=True)
    result = agent.execute(text)
    result["transcript"] = text
    return jsonify(result)


def open_browser():
    """সার্ভার চালু হওয়ার ১ সেকেন্ড পর অটোমেটিক ব্রাউজার খোলে।"""
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    port = 5000
    print("\n" + "═" * 65)
    print(" 🚀 JARVIS Universal Voice Dashboard Server")
    print(f" 🌐 URL: http://127.0.0.1:{port}")
    print(" 🎤 বাংলা ভয়েস ও পিসি কন্ট্রোল সক্রিয়!")
    print("═" * 65 + "\n")

    # ব্রাউজার ওপেন থ্রেড
    threading.Thread(target=open_browser, daemon=True).start()

    # Flask সার্ভার স্টার্ট
    app.run(host="127.0.0.1", port=port, debug=False)
