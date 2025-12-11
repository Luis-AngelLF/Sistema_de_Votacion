/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",          // Necesario para detectar clases en el HTML principal
    "./src/**/*.{js,jsx,ts,tsx}"  // Todas las rutas dentro de src (React)
  ],
  theme: {
    extend: {},  // Aquí puedes agregar colores, fuentes o tamaños personalizados
  },
  plugins: [],  // Plugins de Tailwind, si quieres usar alguno
};
