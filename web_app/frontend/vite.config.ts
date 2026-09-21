import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // Caminho relativo: funciona tanto em github.io/<user>.github.io (raiz) quanto em
  // github.io/<user>/<repo> (subpasta) sem precisar saber o nome do repo de antemão.
  base: './',
  plugins: [react()],
})
