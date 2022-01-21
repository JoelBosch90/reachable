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

.animated-background {
  background: linear-gradient(
    -45deg,
    #FFFFFF,
    #fcedef,
    #DCF1D0,
    #FFFFFF,
    #fcedef,
    #DCF1D0
  );
  background-size: 1000% 1000%;
  animation: gradient 20s ease infinite;
  height: 80%;
}
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
