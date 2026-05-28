/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#020617',
          800: '#09090b',
          700: '#0f172a',
          600: '#1e293b',
        }
      }
    },
  },
  plugins: [],
}
