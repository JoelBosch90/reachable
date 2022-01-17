<template>
  <v-container class="my-8">
    <ResponseForm :link-key="$route.params.key" />
  </v-container>
</template>

<script>
export default {
  layout: 'user'
}
</script>
