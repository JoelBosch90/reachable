<template>
  <div>
    <v-container class="fill-height pa-16">
      <v-row class="mb-8">
        <h1 class="text-center display-4 hidden-xs-only mx-auto">
          Create a form in seconds!
        </h1>
        <h1 class="text-center display-2 hidden-sm-and-up mx-auto">
          Create a form in seconds!
        </h1>
      </v-row>
      <v-container class="mx-auto text">
        <h1 class="display-1">
          Quick contact form
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
            Create a simple form that people can use to send you emails without
            knowing your email address.
            <br><br>
            Get your form in two clicks!
          </p>
          <CreateContactForm @created="onCreated" />
        </div>
      </v-container>
    </v-container>
  </div>
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
