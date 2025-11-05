import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{ts,tsx,mdx}",
    "./components/**/*.{ts,tsx,mdx}",
    "./app/**/*.{ts,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        text: "var(--text)",
        muted: "var(--muted)",
        border: "var(--border)",
        accent: {
          1: "var(--accent-1)",
          2: "var(--accent-2)",
        },
      },
      boxShadow: {
        sm: "var(--shadow-sm)",
        DEFAULT: "var(--shadow-md)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
      },
      borderRadius: {
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica",
          "Arial",
        ],
        mono: [
          "JetBrains Mono",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
        ],
      },
      fontSize: {
        h1: ["64px", { lineHeight: "1.1", fontWeight: "600", letterSpacing: "-0.02em" }],
        h2: ["48px", { lineHeight: "1.2", fontWeight: "600", letterSpacing: "-0.01em" }],
        h3: ["28px", { lineHeight: "1.3", fontWeight: "500" }],
        body: ["18px", { lineHeight: "1.6" }],
        small: ["14px", { lineHeight: "1.5", letterSpacing: "0.01em" }],
      },
      spacing: {
        1: "4px",
        2: "8px",
        3: "12px",
        4: "16px",
        6: "24px",
        8: "32px",
        12: "48px",
        16: "64px",
        20: "80px",
        30: "120px",
      },
      backgroundImage: {
        "solar-gradient": "linear-gradient(90deg, var(--accent-1) 0%, var(--accent-2) 100%)",
      },
      ringColor: {
        DEFAULT: "var(--accent-1)",
      },
    },
  },
  plugins: [
    function ({ addUtilities }: any) {
      addUtilities({
        ".ring-solar": {
          boxShadow: "0 0 0 3px var(--ring)",
        },
      });
    },
  ],
};

export default config;
