<template>
  <v-container class="text">
    <p
      v-if="form.id != 0 && !form.confirmed"
      class="body-1 error--text"
    >
      This form cannot register any responses because it has not yet been
      confirmed by the owner.
      <br><br>
      Are you the owner? Click the link in your inbox!
    </p>
    <h1 class="display-1">
      {{ form.name }}
    </h1>
    <p
      v-if="error"
      class="body-1 error--text"
    >
      {{ error }}
    </p>
    <div v-else-if="!responded">
      <p class="body-1">
        {{ form.description }}
      </p>
      <Form
        ref="form"
        v-model="form"
        @submit="respond"
      >
        <FormInput
          v-for="input in form.inputs"
          :key="input.name"
          v-model="response[input.name]"
          :label="input.name"
          :hint="input.title"
          :required="true"
          type="textarea"
        />
      </Form>
    </div>
    <p
      v-else
      class="body-1"
    >
      Your response has been sent to the form's owner.
      <br>
      Thank you for responding!
    </p>
  </v-container>
</template>

<script>
export default {
  props: {
    linkKey: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      // This is the data that describes the form that should be displayed.
      form: {
        name: '',
        description: '',
        id: 0,
        inputs: [],
        confirmed: false
      },
      // This is the input that the user has added to the form.
      response: {},
      responded: false,
      error: ''
    }
  },
  watch: {
    linkKey: {
      immediate: true,
      // Try to load the
      handler: 'load'
    }
  },
  mounted () {
    // Immediately load the form if we already have a link key.
    this.load()
  },
  methods: {
    // Method to load the form from from the server.
    async load () {
      // Don't try to load anything without a link key.
      if (this.linkKey) {
        // Get the information about the form.
        const response = await this.$axios.get('forms/link/' + this.linkKey)

        // If we cannot get the form, we redirect to the error page.
        if (!response || !response.data) {
          this.$router.push({ name: 'error-notfound' })

        // Otherwise, extract the data from the response to populate the form.
        } else { this.form = JSON.parse(response.data) }
      }
    },
    // Method to send a response with the current form submission.
    async respond () {
      // Send the response.
      const response = await this.$axios.post('forms/response/', {
        link: this.linkKey,
        inputs: this.response
      })

      // If we got a valid response, we can show the user that the response has
      // been properly processed.
      if (response && response.data) {
        this.responded = true

      // If we didn't get a valid response, something went wrong server-side.
      // We should tell the user that something has gone wrong.
      } else {
        this.$refs.form.showError('Error occurred: your response could not' +
                                  ' be sent.')
      }
    }
  }
}
</script>
