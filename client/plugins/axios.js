/**
 *  This file contains extra configurations for Axios.
 */

// Import dependencies.
import axios from 'axios'

// Make sure we read the CSRF token from the cookie and send it with the correct
// header.
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

// We can use this export to also set the axios defaults for the axios object
// that Nuxt injects into Vue.
export default function ({ $axios }) {
  // Make sure we read the CSRF token from the cookie and send it with the
  // correct header.
  $axios.defaults.xsrfCookieName = 'csrftoken'
  $axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
}
