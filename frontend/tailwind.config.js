const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      fontFamily: {
       sans: ["Inter", ...defaultTheme.fontFamily.sans],
       mono: ["Fira Code", ...defaultTheme.fontFamily.mono],
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    styled: true,
    logs: false,
    themes: [
      {
        mytheme: {
          primary: "#ff6600",
          // more reddish
          "primary-focus": "#e64d00", 
          secondary: "#f6d860",
          accent: "#37cdbe",
          neutral: "#444",
          "success": "#37cdbe",
          "success-focus": "#2aa79b",
          "warning": "#f6d860",
          "warning-focus": "#f3cc00",
          "error": "#ff6600",
          "error-focus": "#e64d00",
          // softer pink
          "info": "#ff8c94",
          "base-100": "#111",
          "base-200": "#222",
          "base-300": "#333",
          "base-400": "#444",
          "--rounded-box": "0rem", // border radius rounded-box utility class, used in card and other large boxes
          "--rounded-btn": "0rem", // border radius rounded-btn utility class, used in buttons and similar element
          "--rounded-badge": "0rem", // border radius rounded-badge utility class, used in badges and similar
          "--animation-btn": "0.25s", // duration of animation when you click on button
          "--animation-input": "0.2s", // duration of animation for inputs like checkbox, toggle, radio, etc
          "--btn-text-case": "uppercase", // set default text transform for buttons
          "--btn-focus-scale": "0.95", // scale transform of button when you focus on it
          "--border-btn": "1px", // border width of buttons
          "--tab-border": "1px", // border width of tabs
          "--tab-radius": "0rem", // border radius of tabs
        },
      },
    ],
    base: true,
    utils: true,
    rtl: false,
    prefix: "",
    darkTheme: "dark",
  },
};
