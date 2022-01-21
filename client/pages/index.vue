<template>
  <div>
    <v-container class="fill-height pa-16">
      <v-row class="mb-8">
        <h1 class="text-center display-4 hidden-xs-only mx-auto">
          Create new forms in seconds!
        </h1>
        <h1 class="text-center display-2 hidden-sm-and-up mx-auto">
          Create new forms in seconds!
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
            Let people contact you through a simple form. All responses are
            automatically sent to your inbox and respondents will never know
            your email address!
            <br><br>
            Create your form in a single click!
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
