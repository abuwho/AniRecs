// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    "@nuxt/ui", 
    "@pinia/nuxt", 
    '@nuxt/image',
  ],

  runtimeConfig: {
    public: {
      apiBase: "http://localhost:8000"
    }
  },

  css: ['~/assets/css/main.css'],
  
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
})