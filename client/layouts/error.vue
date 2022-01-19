<template>
  <v-sheet>
    <ErrorExpired v-if="error.statusCode === 410" />
    <ErrorNotFound v-else-if="error.statusCode === 404" />
    <ErrorNotAllowed v-else-if="error.statusCode === 403" />
    <v-container
      v-else
      class="my-8 mx-auto text"
    >
      <h1 class="display-1 mb-4">
        Unknown error
      </h1>
      <p class="body-1">
        An unknown error has occurred. Unfortunately, we also have no idea what
        happened or how you got here.
      </p>
      <v-btn
        color="primary"
        to="/"
      >
        Take me home
      </v-btn>
    </v-container>
  </v-sheet>
</template>

<script>
export default {
  props: {
    error: {
      type: Object,
      default () {
        return {
          statusCode: 0
        }
      }
    }
  }
}
</script>
