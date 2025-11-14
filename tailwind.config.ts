import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      backgroundImage: {
        "gradient-stellar": "linear-gradient(135deg, hsl(239, 84%, 60%), hsl(262, 83%, 58%), hsl(330, 81%, 60%))",
        "gradient-stella": "linear-gradient(135deg, hsl(239, 84%, 67%), hsl(262, 83%, 65%), hsl(330, 81%, 67%))",
        "gradient-max": "linear-gradient(135deg, hsl(210, 100%, 56%), hsl(188, 94%, 43%), hsl(174, 72%, 56%))",
        "gradient-nova": "linear-gradient(135deg, hsl(25, 95%, 63%), hsl(0, 84%, 60%), hsl(330, 81%, 67%))",
        "gradient-darwin": "linear-gradient(135deg, hsl(142, 76%, 36%), hsl(160, 84%, 39%), hsl(174, 72%, 56%))",
        "gradient-lexis": "linear-gradient(135deg, hsl(271, 91%, 65%), hsl(262, 83%, 58%), hsl(320, 86%, 52%))",
        "gradient-neo": "linear-gradient(135deg, hsl(215, 28%, 17%), hsl(215, 20%, 65%), hsl(240, 6%, 52%))",
        "gradient-luna": "linear-gradient(135deg, hsl(45, 93%, 47%), hsl(25, 95%, 63%), hsl(0, 84%, 60%))",
        "gradient-atlas": "linear-gradient(135deg, hsl(43, 96%, 56%), hsl(25, 95%, 63%), hsl(0, 84%, 60%))",
      },
      keyframes: {
        "accordion-down": {
          from: {
            height: "0",
          },
          to: {
            height: "var(--radix-accordion-content-height)",
          },
        },
        "accordion-up": {
          from: {
            height: "var(--radix-accordion-content-height)",
          },
          to: {
            height: "0",
          },
        },
        floating: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-20px)" },
        },
        glow: {
          "0%": { boxShadow: "0 0 20px hsl(262 83% 58% / 0.3)" },
          "100%": { boxShadow: "0 0 40px hsl(262 83% 58% / 0.6)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        floating: "floating 3s ease-in-out infinite",
        glow: "glow 2s ease-in-out infinite alternate",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
