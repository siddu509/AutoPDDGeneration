import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/generate-pdd': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/upload-and-process': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/api/': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/refine-section': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/chat': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
