/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ntu-red': '#E01932',
        'ntu-red-hover': '#C2142A',
        'ntu-blue': '#0071BC',
        'ntu-gold': '#F79320',
        'ntu-dark': '#2D2D2D',
        'ntu-body': '#4A4A4A',
        'ntu-muted': '#888888',
        'ntu-border': '#E5E5E5',
        // Keep old names as aliases for backward compat in existing chat components
        'nbs-red': '#E01932',
        'nbs-red-dark': '#C2142A',
        'nbs-gold': '#F79320',
      },
    },
  },
  plugins: [],
}
