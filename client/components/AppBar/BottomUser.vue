<template>
  <v-footer
    dark
    padless
  >
    <v-card
      class="flex"
      flat
      tile
    >
      <v-card-text class="text-center">
        <span
          class="body-1 hidden-xs-only"
        >
          Do you also want to create nifty forms like this one? Visit the links
          below to find out how!
        </span>
        <span
          class="body-1 hidden-sm-and-up"
        >
          Also want a form? Click below!
        </span>
      </v-card-text>

      <v-card-title class="grey darken-2">
        <v-toolbar-items class="mx-auto">
          <v-btn
            v-for="item in items"
            :key="item.title"
            :to="item.link"
            text
          >
            <v-icon small left>
              {{ item.icon }}
            </v-icon>
            <span
              class="hidden-xs-only"
            >
              {{ item.title }}
            </span>
          </v-btn>
        </v-toolbar-items>
      </v-card-title>

      <v-card-text class="py-2 white--text text-center">
        {{ new Date().getFullYear() }} — <strong>Reachable</strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {
  data () {
    return {
      items: [
        { title: 'Home', link: '/', icon: 'mdi-home' },
        { title: 'Custom', link: '/form/custom', icon: 'mdi-pencil' },
        { title: 'About', link: '/about', icon: 'mdi-information' }
      ]
    }
  }
}
</script>
