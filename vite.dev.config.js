import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import reactRefresh from "@vitejs/plugin-react-refresh"


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), reactRefresh()],
  root: "./Pulmo9-Frontend",
  //base: "/assets",
  build: {
    outDir: "../web/assets",
    assetsDir: "/assets",
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: undefined,
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]',

      },
      input: {
        'app': './Pulmo9-Frontend/main.jsx',
      }
    },
  },
})