"""
JARVIS Quick Setup & Launcher
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("""
╔═══════════════════════════════════════╗
║     JARVIS — Voice PC Control Setup   ║
╚═══════════════════════════════════════╝
""")

# Check .env
env_file = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(env_file):
    print("[!] .env ফাইল নেই।")
    key = input("আপনার Gemini API Key লিখুন (Enter দিলে skip): ").strip()
    if key:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"GEMINI_API_KEY={key}\n")
        print("[✓] .env ফাইল তৈরি হয়েছে।")
else:
    print("[✓] .env ফাইল পাওয়া গেছে।")

# Install dependencies
print("\n[*] Dependencies install করা হচ্ছে...")
os.system("pip install -r requirements.txt --quiet")
os.system("pip install pygame-ce --quiet")
print("[✓] Install সম্পন্ন।")

print("""
[✓] Setup সম্পন্ন! JARVIS ব্যবহারের ২টি মাধ্যম আছে:

 1️⃣ 🌐 Web Dashboard (সবচেয়ে সহজ — ভিজ্যুয়াল ইন্টারফেস ও ভয়েস কন্ট্রোল):
     কমান্ড: python server.py
     ওয়েব লিংক: http://127.0.0.1:5000
     (ব্রাউজার অটোমেটিক খুলে যাবে, মাইক অন করলেই কথা বলে ফুল পিসি কন্ট্রোল করতে পারবেন)

 2️⃣ 💻 Terminal Assistant Mode:
     কমান্ড: python jarvis.py
""")
