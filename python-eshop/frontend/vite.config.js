import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const API_PORT = 8765;
const FRONTEND_PORT = 4321;

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: FRONTEND_PORT,
    strictPort: true,
    proxy: {
      '/api': `http://127.0.0.1:${API_PORT}`,
      '/static': `http://127.0.0.1:${API_PORT}`,
    },
  },
});
