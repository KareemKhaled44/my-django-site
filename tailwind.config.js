/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./**/*.html", "./**/*.js"],
  theme: {
    extend: {
      colors: {
        gold: "#b9a848",
        dark: "#28282B",
        darker: "#1E1E1E",
        light: "#F9FAFB",
      },
      fontFamily: {
        montserrat: ["Montserrat", "serif"],
      },
    },
  },
  plugins: [],
};