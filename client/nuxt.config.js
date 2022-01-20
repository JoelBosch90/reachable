export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'reachable',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    // Import our own styles.
    '~/assets/styles/main.scss'
  ],

  // Make sure we reload when SCSS files are changed.
  watch: ['~/assets/*.scss'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/axios'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',

    // Simple usage
    '@nuxtjs/vuetify'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Fallback base URL for API calls.
    baseUrl: 'http://localhost:8004/api/'
  },

  // This part of the configuration is accessible both to the client and the
  // server.
  publicRuntimeConfig: {
    // Base URL for API calls.
    axios: {
      baseURL: process.env.API_URL
    }
  },

  // This part of the configuration is accessible to the server only.
  privateRuntimeConfig: {
  },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en'
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
