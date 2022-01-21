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

/* Create a subtle animated background to make design more interesting. */
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
  animation: back-and-forth 20s ease infinite;
  height: 80%;
}
/* Simple back and forth animation for the background. */
@keyframes back-and-forth {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
