/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Warm editorial palette
        warm: {
          50:  '#FAF7F2',
          100: '#F0EBE1',
          200: '#E4DDD0',
          300: '#C9BFAE',
          400: '#A89A86',
          500: '#8A7C68',
          600: '#6B5D4A',
          700: '#4D4234',
          800: '#332C22',
          900: '#1A1612',
        },
        ink: {
          DEFAULT: '#1A1612',
          soft: '#4D4234',
          muted: '#8A7C68',
        },
        accent: {
          gold: '#C4973B',
          rust: '#A0522D',
          sage: '#6B7F5E',
          navy: '#2C3E50',
        },
      },
      fontFamily: {
        pixel: ['"Press Start 2P"', 'monospace'],
        serif: ['"Crimson Text"', 'Georgia', 'serif'],
        mono: ['"Courier New"', 'monospace'],
      },
    },
  },
  plugins: [],
}
