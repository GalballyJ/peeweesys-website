/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        pw: {
          bg: '#141619',
          panel: '#1C1F24',
          surface: '#22262C',
          card: '#181A1E',
          line: '#2E333B',
          line2: '#25292F',
          text: '#F3F4F5',
          muted: '#9AA0A6',
          red: '#FF3B4E',
          guardsred: '#E3172C',
          'red-muted': '#3D1015',
          green: '#2FBF71',
          'green-muted': '#0D331E',
          amber: '#FFB020',
          'amber-muted': '#3D2E0B',
          blue: '#38BDF8',
          'blue-muted': '#0B2A3D',
        },
      },
      fontFamily: {
        sans: ['Barlow Semi Condensed', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Consolas', 'Courier New', 'monospace'],
      },
      boxShadow: {
        'glow-red': '0 0 24px -4px rgba(227, 23, 44, 0.45)',
        'glow-green': '0 0 24px -4px rgba(47, 191, 113, 0.35)',
        'glow-amber': '0 0 24px -4px rgba(255, 176, 32, 0.35)',
      },
      backgroundImage: {
        'radial-fade': 'radial-gradient(circle at top, rgba(227, 23, 44, 0.12) 0%, rgba(20, 22, 25, 0) 70%)',
      },
    },
  },
  plugins: [],
};
