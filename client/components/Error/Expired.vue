<template>
  <v-container class="my-8 mx-auto text">
    <h1 class="display-1 mb-4">
      Expired link
    </h1>
    <p class="body-1">
      Unfortunately, the link you tried to visit can no longer be used.
    </p>
    <h2 class="display-1 mb-4 mt-8">
      Why do links expire?
    </h2>
    <p class="body-1">
      There are several reasons why links may expire:
    </p>
    <ul class="body-1">
      <li>
        To prevent unexpected responses to long forgotten forms.
      </li>
      <li>
        To help prevent malicious access with long forgotten access links.
      </li>
    </ul>
    <v-btn
      class="mt-8"
      color="info"
      to="/"
    >
      Take me home
    </v-btn>
  </v-container>
</template>
