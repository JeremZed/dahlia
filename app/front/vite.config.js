import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import dotenv from 'dotenv'

const envPath = path.resolve(__dirname, '.env');
dotenv.config({ path: envPath });

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: true
  },
  define: {
    'process.env': process.env
  }
})