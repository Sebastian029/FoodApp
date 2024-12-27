/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./src/**/*.{js,jsx,ts,tsx}", // This covers all files in src directory
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1B3358",
        accent: "#FDB347",
      },
    },
  },
};
