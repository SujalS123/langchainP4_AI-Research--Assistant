/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pastel: {
          pink: '#FFD6E0',
          blue: '#D6E5FF',
          purple: '#E6D6FF',
          green: '#D6FFE6',
          yellow: '#FFF5D6',
          orange: '#FFE5D6',
          mint: '#D6FFF5',
          lavender: '#F0E6FF',
          peach: '#FFE6D6',
          sky: '#E6F5FF',
        },
        accent: {
          pink: '#FF6B9D',
          blue: '#6B9DFF',
          purple: '#9D6BFF',
          green: '#6BFF9D',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      }
    },
  },
  plugins: [],
}
