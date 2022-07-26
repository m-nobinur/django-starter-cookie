/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./templates/**/*.html", "./node_modules/flowbite/**/*.js", "./apps/**/utils.py"],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
};
