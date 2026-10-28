"""
JARVIS Memory & Daily Task Engine
SQLite ভিত্তিক দীর্ঘমেয়াদী স্মৃতি ও দৈনিক কাজের ট্র্যাকার।
ব্যবহারকারী যা বলে তা মনে রাখা, সারাদিনের কাজের তালিকা রাখা ও হিসাব দেওয়া।
"""

import os
import sqlite3
import datetime
from pathlib import Path


class MemoryEngine:
    def __init__(self, db_path: str = None):
        if not db_path:
            base_dir = Path(__file__).parent.parent
            data_dir = base_dir / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "jarvis_memory.sqlite")

        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. দৈনিক কাজের তালিকা
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_date TEXT NOT NULL,
                    task_desc TEXT NOT NULL,
                    is_done INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME
                )
            """)

            # 2. দীর্ঘমেয়াদী স্মৃতি (যেকোনো তথ্য, নোট, পাসওয়ার্ড বা প্রিয় বিষয়)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 3. চ্যাট হিস্ট্রি
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    @staticmethod
    def _today_str():
        return datetime.date.today().isoformat()

    # ══════════════════════════════════════════════════
    # 📋 DAILY TASKS (দৈনিক কাজের ট্র্যাকিং)
    # ══════════════════════════════════════════════════

    def add_tasks(self, task_descriptions: list, task_date: str = None) -> list:
        """আজকের সারাদিনের নতুন কাজের তালিকা যুক্ত করো।"""
        if not task_date:
            task_date = self._today_str()

        saved = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for desc in task_descriptions:
                clean = desc.strip(" \t\n\r-—•1234567890.০১২৩৪৫৬৭৮৯")
                if len(clean) > 2:
                    cursor.execute(
                        "INSERT INTO daily_tasks (task_date, task_desc, is_done) VALUES (?, ?, 0)",
                        (task_date, clean)
                    )
                    saved.append(clean)
            conn.commit()
        return saved

    def mark_completed(self, query: str, task_date: str = None) -> tuple:
        """
        কোনো কাজ সম্পন্ন হয়েছে হিসেবে মার্ক করো।
        Returns (success: bool, task_name: str)
        """
        if not task_date:
            task_date = self._today_str()

        q_clean = query.lower().strip()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, task_desc FROM daily_tasks WHERE task_date = ? AND is_done = 0",
                (task_date,)
            )
            rows = cursor.fetchall()

            matched_id = None
            matched_name = ""

            # Check exact or partial match
            for r in rows:
                desc = r["task_desc"]
                desc_low = desc.lower()
                # Check keywords
                words = [w for w in q_clean.split() if len(w) > 2 and w not in ["কাজে", "কাজ", "করছি", "করসি", "করেছি", "শেষ", "কমপ্লিট", "done"]]
                if any(w in desc_low for w in words) or (desc_low in q_clean):
                    matched_id = r["id"]
                    matched_name = desc
                    break

            # If still not found and query contains a number (e.g., "১ নম্বর কাজ" or "1st task")
            if not matched_id and rows:
                num_map = {"১": 1, "২": 2, "৩": 3, "৪": 4, "৫": 5, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
                for k, v in num_map.items():
                    if k in q_clean and v <= len(rows):
                        matched_id = rows[v - 1]["id"]
                        matched_name = rows[v - 1]["task_desc"]
                        break

            if matched_id:
                now_str = datetime.datetime.now().isoformat()
                cursor.execute(
                    "UPDATE daily_tasks SET is_done = 1, completed_at = ? WHERE id = ?",
                    (now_str, matched_id)
                )
                conn.commit()
                return True, matched_name

        return False, ""

    def get_tasks_summary(self, task_date: str = None) -> dict:
        """আজকের মোট কাজ, সম্পন্ন কাজ ও বাকি কাজের হিসাব দেয়।"""
        if not task_date:
            task_date = self._today_str()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT task_desc, is_done, completed_at FROM daily_tasks WHERE task_date = ? ORDER BY id ASC",
                (task_date,)
            )
            rows = cursor.fetchall()

            completed = [r["task_desc"] for r in rows if r["is_done"] == 1]
            pending = [r["task_desc"] for r in rows if r["is_done"] == 0]

            return {
                "date": task_date,
                "total": len(rows),
                "completed": completed,
                "pending": pending
            }

    # ══════════════════════════════════════════════════
    # 🧠 GENERAL LONG-TERM MEMORY (স্মৃতি সংরক্ষণ)
    # ══════════════════════════════════════════════════

    def remember(self, content: str, topic: str = "general") -> bool:
        """যেকোনো তথ্য স্মৃতিতে সেভ করো।"""
        clean = content.strip()
        if not clean:
            return False

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memories (topic, content) VALUES (?, ?)",
                (topic, clean)
            )
            conn.commit()
            return True

    def recall(self, query: str = "") -> list:
        """স্মৃতি থেকে তথ্য খুঁজে বের করো।"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if not query:
                cursor.execute("SELECT id, topic, content, created_at FROM memories ORDER BY id DESC LIMIT 10")
            else:
                q_words = [w for w in query.lower().split() if len(w) > 2]
                if q_words:
                    like_clauses = " OR ".join(["content LIKE ?" for _ in q_words])
                    params = [f"%{w}%" for w in q_words]
                    cursor.execute(f"SELECT id, topic, content, created_at FROM memories WHERE {like_clauses} ORDER BY id DESC LIMIT 5", params)
                else:
                    cursor.execute("SELECT id, topic, content, created_at FROM memories ORDER BY id DESC LIMIT 5")

            rows = cursor.fetchall()
            return [{"id": r["id"], "topic": r["topic"], "content": r["content"], "created_at": r["created_at"]} for r in rows]

    # ══════════════════════════════════════════════════
    # 💬 CHAT HISTORY
    # ══════════════════════════════════════════════════

    def log_chat(self, role: str, content: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (role, content) VALUES (?, ?)",
                (role, content)
            )
            conn.commit()

    def get_recent_chat(self, limit: int = 6) -> list:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM chat_history ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    def get_ai_memory_context(self) -> str:
        """Gemini AI এর প্রম্পটে যুক্ত করার জন্য বর্তমান স্মৃতি ও কাজের কনটেক্সট।"""
        today_summary = self.get_tasks_summary()
        recent_memories = self.recall()

        parts = []
        if today_summary["total"] > 0:
            parts.append(f"আজকের কাজের হিসাব ({today_summary['date']}):")
            if today_summary["completed"]:
                parts.append("  সম্পন্ন কাজ: " + ", ".join(today_summary["completed"]))
            if today_summary["pending"]:
                parts.append("  বাকি কাজ: " + ", ".join(today_summary["pending"]))

        if recent_memories:
            mem_items = [m["content"] for m in recent_memories[:5]]
            parts.append("ব্যবহারকারীর সংরক্ষিত স্মৃতি ও নোট: " + " | ".join(mem_items))

        return "\n".join(parts)
