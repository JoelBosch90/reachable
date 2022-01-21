<template>
  <v-container class="my-8 text mx-auto">
    <h1 class="display-1">
      Create a custom form
    </h1>
    <div v-if="created">
      <p class="body-1">
        Your contact form has been created.
        <br><br>
        View your inbox for the link!
      </p>
    </div>
    <div v-else>
      <p class="body-1">
        Do you want more control over your form? Create a form and with a name
        and description that you decide!
      </p>
      <CreateCustomForm @created="onCreated" />
    </div>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      created: false
    }
  },
  methods: {
    // Method to call when a new form was created.
    onCreated () {
      // Show the user.
      this.created = true
    }
  }
}
</script>
