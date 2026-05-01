/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          purple: '#6366f1', // 深空紫
          gold: '#F59E0B',   // 卡密金
        },
        secondary: {
          blue: '#3b82f6',   // 星空蓝
        },
        accent: {
          gold: '#fbbf24',    // 金色 (卡密)
        },
        status: {
          success: '#10B981', // 隐私绿
          danger: '#ef4444',  // 错误红
        },
        bg: {
          dark: '#0f172a',    // 深空背景
        }
      },
      backgroundImage: {
        'gold-gradient': 'linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)',
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
