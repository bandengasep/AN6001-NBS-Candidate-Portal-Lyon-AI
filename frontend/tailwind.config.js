/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // NBS brand colors
        'nbs-red': '#C8102E',
        'nbs-red-dark': '#A00D24',
        'nbs-gold': '#B4975A',
      },
    },
  },
  plugins: [],
}
