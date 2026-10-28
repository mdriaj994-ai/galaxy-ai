"""
╔══════════════════════════════════════════════════════════════════╗
║         JARVIS - Just A Rather Very Intelligent System          ║
║       AI Voice PC Control — Powered by Google Gemini            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Windows Terminal UTF-8 Encoding Fix
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from core.assistant import JarvisAssistant
from core.display import Display
from config.settings import Settings


def print_banner():
    """Print the JARVIS startup banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║       ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗              ║
    ║       ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝              ║
    ║       ██║███████║██████╔╝██║   ██║██║███████╗              ║
    ║  ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║              ║
    ║  ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║              ║
    ║   ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝              ║
    ║                                                              ║
    ║         Just A Rather Very Intelligent System               ║
    ║    🎤 Full Voice PC Control — বাংলা ও ইংরেজি               ║
    ║           Powered by Google Gemini AI                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print("\033[96m" + banner + "\033[0m")


def main():
    """Main entry point for JARVIS."""
    print_banner()

    # Load settings
    settings = Settings()

    # API key চেক করো (warn করো কিন্তু বন্ধ করো না)
    if not settings.validate():
        print("\033[93m[!] API Key ছাড়া শুধু offline কমান্ড কাজ করবে।\033[0m\n")
    else:
        print("\033[92m[✓] API Key পাওয়া গেছে।\033[0m\n")

    print("\033[93m[*] JARVIS চালু হচ্ছে...\033[0m")
    time.sleep(0.3)

    # Initialize display
    display = Display()

    # Initialize and start assistant
    jarvis = JarvisAssistant(settings, display)

    print("\n\033[92m[✓] JARVIS সম্পূর্ণ প্রস্তুত!\033[0m")
    print("\033[94m[i] ভয়েসে বলুন অথবা টাইপ করুন\033[0m")
    print("\033[94m[i] 'help' লিখলে/বললে সব কমান্ড দেখতে পাবেন\033[0m")
    print("\033[94m[i] বন্ধ করতে: 'বিদায় জারভিস' বা Ctrl+C\033[0m\n")

    try:
        jarvis.run()  # ✅ Fixed: speak() after run() was unreachable before
    except KeyboardInterrupt:
        pass

    # ✅ Fixed: এখন এখানে পৌঁছানো সম্ভব কারণ run() return করে
    print("\n\033[93m[!] JARVIS বন্ধ হচ্ছে...\033[0m")
    sys.exit(0)


if __name__ == "__main__":
    main()
