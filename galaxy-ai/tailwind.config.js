/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        void: '#0B0E14',
        'void-light': '#121722',
        'void-card': '#161D2B',
        cyan: {
          neon: '#00F0FF',
          glow: 'rgba(0, 240, 255, 0.35)',
        },
        purple: {
          electric: '#7000FF',
          glow: 'rgba(112, 0, 255, 0.35)',
        },
      },
      fontFamily: {
        mono: ['Fira Code', 'Courier New', 'monospace'],
        cyber: ['Orbitron', 'Rajdhani', 'sans-serif'],
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 240, 255, 0.45)',
        'neon-purple': '0 0 20px rgba(112, 0, 255, 0.45)',
      },
    },
  },
  plugins: [],
}

