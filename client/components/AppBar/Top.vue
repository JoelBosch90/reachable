<template>
  <nav class="overflow-hidden">
    <v-app-bar
      app
      fixed
    >
      <v-app-bar-title>
        Reachable
      </v-app-bar-title>

      <v-spacer />

      <v-toolbar-items>
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
    </v-app-bar>

    <v-navigation-drawer
      v-model="showDrawer"
      absolute
      temporary
      right
    >
      <v-list>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.link"
        >
          <v-list-item-icon>
            <v-icon small>
              {{ item.icon }}
            </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.title }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
export default {
  props: {
    scrollTarget: {
      type: String,
      default: ''
    }
  },
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
