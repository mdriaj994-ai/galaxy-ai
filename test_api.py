# -*- coding: utf-8 -*-
"""JARVIS ফুল বাংলা ভয়েস ও পিসি কন্ট্রোল টেস্ট সুইট"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = "http://127.0.0.1:5000"

commands = [
    "আজকে কি বার",
    "এখন সময় কত",
    "আজকে কত তারিখ",
    "ব্যাটারি কত",
    "কেমন আছো",
    "তুমি কে",
    "ভলিউম বাড়াও",
    "ভলিউম কমাও",
    "স্ক্রিনশট নাও",
    "ইউটিউবে বাংলা গান বাজাও",
    "ফেসবুক খোলো",
    "ফটোশপ খোলো",
    "ক্যালকুলেটর খোলো",
    "নোটপ্যাড খোলো",
    "সব মিনিমাইজ করো",
    "রিসাইকেল বিন খালি করো"
]

print("=" * 60)
print("  JARVIS বাংলা ভয়েস ও পিসি কমান্ড টেস্ট")
print("=" * 60)

passed = 0
for cmd in commands:
    try:
        r = requests.post(f"{BASE}/api/command", json={"command": cmd}, timeout=5)
        d = r.json()
        status = "✓" if d.get("success") else "✗"
        print(f"[{status}] {cmd:24} => {d.get('reply')} ({d.get('action')})")
        if d.get("success"):
            passed += 1
    except Exception as e:
        print(f"[✗] {cmd:24} => ERROR: {e}")

print("=" * 60)
print(f"  মোট টেস্ট: {len(commands)}, সফল: {passed}")
print("=" * 60)
