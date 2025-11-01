import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        orbit: "#4C6FFF",
        plasma: "#6B3DF4",
        deepspace: "#0A0E29",
        nebula: "#F05AFF",
        teal: "#2DD4BF",
      },
    },
  },
  plugins: [],
};
export default config;
