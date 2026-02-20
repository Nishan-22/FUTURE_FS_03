/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './restaurant/templates/**/*.html',
    './restaurant/static/restaurant/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'cafe-brown': '#8B4513',
        'cafe-light': '#D2B48C',
        'cafe-dark': '#5D2906',
        'cafe-cream': '#FDFBF7',
        'cafe-gold': '#DAA520',
        'cafe-espresso': '#2C1A0F',
        'cafe-mocha': '#A0522D',
        'cafe-latte': '#E6D7C3',
      },
      fontFamily: {
        'serif': ['"Playfair Display"', 'serif'],
        'sans': ['"Lato"', 'sans-serif'],
      }
    },
  },
  plugins: [],
}