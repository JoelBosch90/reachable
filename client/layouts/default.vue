<template>
  <v-app class="theme--light">
    <AppBarTop />
    <v-main class="animated-background">
      <Nuxt />
    </v-main>
    <AppBarBottom />
  </v-app>
</template>

<style>
/* Long lines of text are hard to read, so we like to keep them short. */
.text { max-width: 640px; }
</style>
