import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from config.settings import Settings
from core.commands import CommandProcessor

class MockAssistant:
    spoken = []
    conversation_history = []
    def speak(self, text):
        self.spoken.append(text)
        print(f'  JARVIS: {text}')

s = Settings()
mock = MockAssistant()
cp = CommandProcessor(s, mock)

print('=== Command Processor Tests ===')
tests = [
    'সময় কত',
    'আজ কত তারিখ',
    'কি বার',
    'ভলিউম বাড়াও',
    'ব্যাটারি',
    'গুগলে সার্চ করো python tutorial',
    'ইউটিউবে সার্চ করো bangla song',
]
for t in tests:
    result = cp.process(t)
    status = 'OK' if result else 'NO'
    print(f'  [{status}] "{t}"')

print('\n=== Safe Math Tests ===')
math_tests = [
    ('calculate 5 plus 3', 8),
    ('calculate 10 times 5', 50),
    ('what is 100 divided by 4', 25.0),
]
for expr, expected in math_tests:
    cp.process(expr)

print('\nAll tests done!')
