"""
JARVIS Display Module
টার্মিনালে সুন্দর আউটপুট দেখায়।
"""

import sys
import datetime


class Display:
    """টার্মিনাল ডিসপ্লে পরিচালনা করে।"""
    
    # ANSI রঙ কোড
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    GREY = "\033[90m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    def jarvis_response(self, text: str):
        """JARVIS এর উত্তর সুন্দরভাবে দেখাও।"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n{self.CYAN}┌─[JARVIS {timestamp}]─────────────────────────")
        print(f"│ {self.WHITE}{text}")
        print(f"{self.CYAN}└──────────────────────────────────────────{self.RESET}")
    
    def user_input(self, text: str):
        """ব্যবহারকারীর ইনপুট দেখাও।"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n{self.GREEN}◆ You [{timestamp}]: {self.WHITE}{text}{self.RESET}")
    
    def listening_indicator(self):
        """শোনার অ্যানিমেশন দেখাও।"""
        print(f"\n{self.BLUE}  🎤 Listening...{self.RESET}", end="\r")
    
    def thinking_indicator(self):
        """চিন্তার অ্যানিমেশন দেখাও।"""
        print(f"\n{self.YELLOW}  🤔 Thinking...{self.RESET}", end="\r")
    
    def error(self, message: str):
        """ত্রুটি বার্তা দেখাও।"""
        print(f"\n{self.RED}[ERROR] {message}{self.RESET}")
    
    def info(self, message: str):
        """তথ্য বার্তা দেখাও।"""
        print(f"\n{self.GREY}[INFO] {message}{self.RESET}")
    
    def success(self, message: str):
        """সফলতার বার্তা দেখাও।"""
        print(f"\n{self.GREEN}[✓] {message}{self.RESET}")
    
    def separator(self):
        """বিভাজক রেখা আঁকো।"""
        print(f"\n{self.GREY}" + "─" * 60 + f"{self.RESET}")
