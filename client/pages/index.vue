<template>
  <v-sheet>
    <v-container class="fill-height pa-16">
      <v-row>
        <h1 class="text-center display-4 hidden-xs-only">
          Create new forms in seconds!
        </h1>
        <h1 class="text-center display-2 hidden-sm-and-up">
          Create new forms in seconds!
        </h1>
      </v-row>
    </v-container>
    <v-container class="my-8 mx-auto text">
      <h1 class="display-1">
        Quick contact form
      </h1>
      <p class="body-1">
        Let people contact you through a simple form. All responses are
        automatically sent to your inbox and respondents will never know your
        email address!
      </p>
      <p class="body-1">
        Create your form in a single click!
      </p>
      <ShareForm
        v-if="linkKey"
        :link-key="linkKey"
      />
      <ContactForm
        v-else
        @created="onCreated"
      />
    </v-container>
  </v-sheet>
</template>

<script>
export default {
  data () {
    return {
      linkKey: ''
    }
  },
  methods: {
    // Method to call when a new form was created.
    onCreated (key) {
      // Store the key.
      this.linkKey = key
    }
  }
}
</script>
