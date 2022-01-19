<template>
  <v-container class="my-8">
    <ResponseForm :form-key="$route.params.key" />
  </v-container>
</template>

<script>
export default {
  layout: 'user'
}
</script>
