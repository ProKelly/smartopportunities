/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        // "Night chart" palette — a navigator's chart at dusk.
        navy: {
          950: "#0B0F1F",
          900: "#12172B",
          800: "#1B2140",
          700: "#262E52",
          600: "#333C68",
        },
        parchment: "#F6F4EC",
        signal: {
          DEFAULT: "#F2B84B", // beacon gold — primary accent
          dim: "#C9922E",
        },
        chart: {
          DEFAULT: "#4FD1C5", // charted-route teal — secondary accent
          dim: "#2E9A90",
        },
        coral: "#EF7B6A", // deadlines / urgency
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      backgroundImage: {
        "star-field":
          "radial-gradient(circle at 20% 20%, rgba(242,184,75,0.08), transparent 35%), radial-gradient(circle at 80% 0%, rgba(79,209,197,0.10), transparent 40%), radial-gradient(circle at 50% 100%, rgba(79,209,197,0.06), transparent 45%)",
      },
      boxShadow: {
        beacon: "0 0 0 1px rgba(242,184,75,0.25), 0 8px 30px -8px rgba(242,184,75,0.35)",
        chart: "0 8px 30px -12px rgba(0,0,0,0.5)",
      },
    },
  },
  plugins: [],
};
