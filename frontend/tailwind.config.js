const defaultTheme = require('tailwindcss/defaultTheme');


/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        spaceg: ['"Space Grotesk"', ...defaultTheme.fontFamily.sans]
      }
    }
  },
  plugins: [require("daisyui"),], 
  darkMode: ["selector", "[data-theme*='dark']"],
}

