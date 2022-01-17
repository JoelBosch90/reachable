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
        <span class="body-1">
          Do you also want to create nifty forms like this one? Visit the links
          below to find out how!
        </span>
      </v-card-text>

      <v-card-title class="grey darken-2">
        <v-toolbar-items class="mx-auto">
          <v-btn
            v-for="item in items"
            :key="item.title"
            :to="item.link"
            class="hidden-xs-only"
            text
          >
            <v-icon small left>
              {{ item.icon }}
            </v-icon>
            {{ item.title }}
          </v-btn>
          <v-btn
            class="hidden-sm-and-up"
            text
            @click.stop="showDrawer = !showDrawer"
          >
            <v-icon small left>
              mdi-menu
            </v-icon>
            Menu
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
      showDrawer: false,
      items: [
        { title: 'Home', link: '/', icon: 'mdi-home' },
        { title: 'Custom', link: '/form/custom', icon: 'mdi-pencil' },
        { title: 'About', link: '/about', icon: 'mdi-information' }
      ]
    }
  }
}
</script>
