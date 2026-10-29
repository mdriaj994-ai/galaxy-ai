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
    Cartesia AI Ultra-realistic Neural Speech দিয়ে বাস্তব মানুষের কণ্ঠে কথা বলা।
    ডিফল্ট: Cartesia Voice ID: 09ff9493-419d-45fc-937d-411115824bfc (My Zentic Voice)
    ব্যাকআপ: Microsoft Edge Neural TTS
    """
    text = request.args.get("text", "").strip()
    req_voice = request.args.get("voice", "").strip()
    rate = request.args.get("rate", "+0%").strip()
    pitch = request.args.get("pitch", "+0Hz").strip()

    print(f"\n\033[93m[API TTS Request]:\033[0m text='{text}', req_voice='{req_voice}'", flush=True)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    clean_text = speech_engine._clean_text(text) if speech_engine else text
    if not clean_text:
        clean_text = text

    # 1. Cartesia AI Voice চেষ্টা করো
    cartesia_key = getattr(settings, 'CARTESIA_API_KEY', '') or os.getenv('CARTESIA_API_KEY', '')
    cartesia_voice_id = getattr(settings, 'CARTESIA_VOICE_ID', '09ff9493-419d-45fc-937d-411115824bfc') or os.getenv('CARTESIA_VOICE_ID', '09ff9493-419d-45fc-937d-411115824bfc')
    if req_voice and len(req_voice) > 20 and "-" in req_voice:
        cartesia_voice_id = req_voice
    cartesia_model = getattr(settings, 'CARTESIA_MODEL', 'sonic-3.6')

    is_edge_voice = req_voice and (req_voice.startswith("bn-") or req_voice.startswith("en-") or req_voice == "edge-tts")
    print(f"[*] cartesia_key present: {bool(cartesia_key)}, is_edge_voice: {is_edge_voice}, cartesia_voice_id: {cartesia_voice_id}", flush=True)
    if cartesia_key and not is_edge_voice:
        try:
            import requests
            import io
            ascii_ratio = sum(1 for c in clean_text if ord(c) < 128) / max(len(clean_text), 1)
            lang = "en" if ascii_ratio > 0.8 else "bn"

            print(f"[*] Calling Cartesia with voice='{cartesia_voice_id}' lang='{lang}'...", flush=True)
            c_resp = requests.post(
                'https://api.cartesia.ai/tts/bytes',
                headers={
                    'Cartesia-Version': '2024-06-10',
                    'X-API-Key': cartesia_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'model_id': cartesia_model,
                    'transcript': clean_text,
                    'voice': {'mode': 'id', 'id': cartesia_voice_id},
                    'output_format': {'container': 'mp3', 'encoding': 'mp3', 'sample_rate': 44100},
                    'language': lang
                },
                timeout=10
            )
            print(f"[*] Cartesia status: {c_resp.status_code}, length: {len(c_resp.content)}", flush=True)
            if c_resp.status_code == 200 and len(c_resp.content) > 1000:
                resp = send_file(
                    io.BytesIO(c_resp.content),
                    mimetype="audio/mpeg",
                    as_attachment=False,
                    download_name="reply.mp3"
                )
                resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                resp.headers["Pragma"] = "no-cache"
                resp.headers["Expires"] = "0"
                resp.headers["X-TTS-Engine"] = f"Cartesia-{cartesia_voice_id[:8]}"
                return resp
            else:
                print(f"[Cartesia TTS Warning]: Status {c_resp.status_code}, falling back to Edge TTS", flush=True)
        except Exception as ce:
            print(f"[Cartesia TTS Error]: {ce}, falling back to Edge TTS", flush=True)

    # 2. ফলব্যাক: Microsoft Edge Neural TTS
    try:
        import io
        import asyncio
        import edge_tts

        ascii_ratio = sum(1 for c in clean_text if ord(c) < 128) / max(len(clean_text), 1)
        if req_voice and (req_voice.startswith("bn-") or req_voice.startswith("en-")):
            voice = req_voice
        elif ascii_ratio > 0.8:
            voice = 'en-US-ChristopherNeural'
        else:
            voice = 'bn-IN-BashkarNeural'

        async def _gen():
            comm = edge_tts.Communicate(clean_text, voice, rate=rate, pitch=pitch)
            data = b""
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    data += chunk["data"]
            return data

        audio_bytes = asyncio.run(_gen())
        resp = send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="reply.mp3"
        )
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        resp.headers["X-TTS-Engine"] = "Edge-TTS"
        return resp
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
    app.run(host="0.0.0.0", port=port, debug=False)
