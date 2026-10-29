"""
JARVIS AI Brain - Google Gemini সংযোগ (সংশোধিত)
এই মডিউল AI থেকে স্মার্ট উত্তর নিয়ে আসে।
"""

import os
import sys
import time
import random

# Windows Terminal UTF-8 Encoding Fix
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


class AIBrain:
    """AI API সংযোগ পরিচালনা করে।"""

    def __init__(self, settings):
        self.settings = settings
        self.provider = settings.AI_PROVIDER
        self.client = None
        self.chat = None
        self._use_legacy = False
        self._initialized = False
        self._initialize()

    def _initialize(self):
        """AI Provider সংযুক্ত করো।"""
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "openai":
            self._init_openai()
        else:
            print(f"\033[91m[Error] অজানা AI Provider: {self.provider}\033[0m")

    def _init_gemini(self):
        """Google Gemini সংযুক্ত করো (নতুন google-genai SDK)।"""
        try:
            from google import genai
            from google.genai import types

            api_key = self.settings.GEMINI_API_KEY
            if not api_key or not api_key.strip():
                print("\033[93m[!] Gemini API Key পাওয়া যায়নি। AI ফিচার সীমিত হবে।\033[0m")
                self.client = None
                return

            self.client = genai.Client(api_key=api_key)
            self._genai_types = types
            self._use_legacy = False
            self._initialized = True
            print("\033[92m  [✓] Google Gemini AI সংযুক্ত হয়েছে!\033[0m")

        except ImportError:
            self._init_gemini_legacy()
        except Exception as e:
            print(f"\033[91m[!] Gemini সংযোগে সমস্যা: {e}\033[0m")
            self._init_gemini_legacy()

    def _init_gemini_legacy(self):
        """পুরনো google-generativeai SDK দিয়ে চেষ্টা করো।"""
        try:
            import google.generativeai as genai
            import warnings
            warnings.filterwarnings("ignore")

            api_key = self.settings.GEMINI_API_KEY
            if not api_key or not api_key.strip():
                self.client = None
                return

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=self.settings.GEMINI_MODEL,
                generation_config={"temperature": 0.7, "max_output_tokens": 512},
                system_instruction=self.settings.SYSTEM_PROMPT,
            )
            self.client = model
            self.chat = model.start_chat(history=[])
            self._use_legacy = True
            self._initialized = True
            print("\033[92m  [✓] Google Gemini AI (legacy) সংযুক্ত হয়েছে!\033[0m")

        except Exception as e:
            print(f"\033[91m[!] Gemini (legacy) সংযোগে সমস্যা: {e}\033[0m")
            self.client = None

    def _init_openai(self):
        """OpenAI সংযুক্ত করো।"""
        try:
            from openai import OpenAI
            api_key = self.settings.OPENAI_API_KEY
            if not api_key:
                print("\033[93m[!] OpenAI API Key পাওয়া যায়নি।\033[0m")
                self.client = None
                return
            self.client = OpenAI(api_key=api_key)
            self._use_legacy = False
            self._initialized = True
            print("\033[92m  [✓] OpenAI সংযুক্ত হয়েছে!\033[0m")

        except ImportError:
            print("\033[91m[!] openai ইনস্টল করুন: pip install openai\033[0m")
            self.client = None
        except Exception as e:
            print(f"\033[91m[!] OpenAI সংযোগে সমস্যা: {e}\033[0m")
            self.client = None

    def get_response(self, user_input: str, history: list = None, context: str = None) -> str:
        """
        AI থেকে উত্তর নিয়ে আসো।

        Args:
            user_input: ব্যবহারকারীর প্রশ্ন
            history: পূর্ববর্তী কথোপকথনের তালিকা
            context: স্মৃতি ও বর্তমান কাজের কনটেক্সট

        Returns:
            AI এর উত্তর
        """
        if not self.client:
            return self._fallback_response(user_input)

        if self.provider == "gemini":
            return self._gemini_response(user_input, history=history, context=context)
        elif self.provider == "openai":
            return self._openai_response(user_input, history)

        return self._fallback_response(user_input)

    def _gemini_response(self, user_input: str, history: list = None, context: str = None) -> str:
        """Gemini থেকে উত্তর নাও — মাল্টিপল মডেল ফলব্যাক + retry সহ।"""
        fallback_models = getattr(
            self.settings, 'GEMINI_FALLBACK_MODELS',
            ['gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.6-flash', 'gemini-3.7-flash']
        )
        primary = getattr(self.settings, 'GEMINI_MODEL', 'gemini-3.5-flash')
        models_to_try = [primary] + [m for m in fallback_models if m != primary]

        # System instruction with Memory context
        sys_instruction = self.settings.SYSTEM_PROMPT
        if context:
            sys_instruction += f"\n\n[গুরুত্বপূর্ণ স্মৃতি ও আজকের কাজের তথ্য]:\n{context}"

        # Combine history if available
        combined_prompt = user_input
        if history and isinstance(history, list) and len(history) > 0:
            hist_str = "\n".join([f"{h.get('role', 'user')}: {h.get('content', '')}" for h in history[-4:]])
            combined_prompt = f"পূর্ববর্তী কথা:\n{hist_str}\n\nবর্তমান প্রশ্ন:\n{user_input}"

        for model_name in models_to_try:
            max_attempts = 3  # 503 এর জন্য ৩বার try
            for attempt in range(max_attempts):
                try:
                    if self._use_legacy:
                        response = self.chat.send_message(combined_prompt)
                        if response and response.text:
                            return response.text.strip()
                    else:
                        from google.genai import types
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=combined_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=sys_instruction,
                                temperature=0.7,
                                max_output_tokens=800,
                            )
                        )
                        if response and response.text:
                            return response.text.strip()
                    break  # সফল

                except Exception as e:
                    err_str = str(e)

                    if '404' in err_str or 'no longer available' in err_str or 'not found' in err_str.lower():
                        # এই মডেল নেই — পরেরটায় যাও
                        break

                    elif '503' in err_str or 'unavailable' in err_str.lower() or 'experimental' in err_str.lower():
                        # Server busy — retry with backoff
                        wait = (attempt + 1) * 1.5
                        if attempt < max_attempts - 1:
                            print(f"\033[93m[~] Server busy, {wait:.0f}s পরে retry ({attempt+1}/{max_attempts})...\033[0m")
                            time.sleep(wait)
                            continue
                        break  # সব retry শেষ — পরের মডেল

                    elif '429' in err_str or 'quota' in err_str.lower() or 'rate' in err_str.lower():
                        time.sleep(2)
                        continue

                    else:
                        break  # অন্য error — পরের মডেল

        return "AI সার্ভারে পৌঁছানো যাচ্ছে না। একটু পরে আবার চেষ্টা করো।"

    def _openai_response(self, user_input: str, history: list = None) -> str:
        """OpenAI থেকে উত্তর নাও।"""
        try:
            messages = [{"role": "system", "content": self.settings.SYSTEM_PROMPT}]
            if history:
                messages.extend(history[-self.settings.MAX_HISTORY:])
            messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=512,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"\033[91m[OpenAI Error] {e}\033[0m")
            return "AI সার্ভারে সমস্যা হচ্ছে। একটু পরে চেষ্টা করো।"

    def _fallback_response(self, user_input: str) -> str:
        """AI না থাকলে বেসিক উত্তর।"""
        user_lower = user_input.lower()

        greetings_bn = ["হ্যালো", "হাই", "কেমন আছো", "কেমন আছেন"]
        greetings_en = ["hello", "hi", "hey", "how are you"]

        if any(w in user_lower for w in greetings_bn + greetings_en):
            return "হ্যালো! আমি জারভিস। এখন আমার AI সংযোগ নেই, তবে basic কমান্ড কাজ করবে।"
        elif any(w in user_lower for w in ["নাম", "name", "who are you", "তুমি কে"]):
            return "আমি জারভিস — Just A Rather Very Intelligent System।"
        elif any(w in user_lower for w in ["joke", "জোকস", "মজা"]):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why was the computer cold? It left its Windows open!",
                "প্রোগ্রামার কাঁদছে কেন? কারণ সে loop থেকে বের হতে পারছে না!",
            ]
            return random.choice(jokes)
        else:
            return (
                "AI চালু করতে GEMINI_API_KEY দরকার। "
                ".env ফাইলে GEMINI_API_KEY=আপনার_key লেখো।"
            )
