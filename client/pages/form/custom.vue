<template>
  <v-container class="my-8 text mx-auto">
    <h1 class="display-1">
      Create a custom form
    </h1>
    <p class="body-1">
      Do you want to create your own contact form, and control its name and its
      description? Look no further: this is what you need!
    </p>
    <CreateCustomForm @created="onCreated" />
  </v-container>
</template>

<script>
export default {
  methods: {
    // Method to call when a new form was created.
    onCreated (key) {
      // Redirect to the share page for this form.
      this.$router.push({
        name: 'form-share-key',
        params: { key }
      })
    }
  }
}
</script>
