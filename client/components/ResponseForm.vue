<template>
  <v-card>
    <v-card-title>
      <h1 class="display-1">
        {{ form.name }}
      </h1>
    </v-card-title>
    <v-card-text
      v-if="error"
    >
      {{ error }}
    </v-card-text>
    <v-card-text
      v-else-if="!responded"
    >
      <p>
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
        />
      </Form>
    </v-card-text>
    <v-card-text
      v-else
    >
      Your response has been sent to the form's owner.
      <br>
      Thank you for responding!
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      // This is the data that describes the form that should be displayed.
      form: {
        name: '',
        description: '',
        id: 0,
        inputs: []
      },
      // This is the input that the user has added to the form.
      response: {},
      responded: false,
      error: ''
    }
  },
  mounted () {
    // Immediately load the form.
    this.load()
  },
  methods: {
    // Method to load the form from from the server.
    async load () {
      try {
        // Get the information about the form.
        const response = await this.$axios.get('forms/link/' +
                                               this.$route.params.key)

        // If we cannot get the form, we should throw an error.
        if (!response || !response.data) {
          throw new Error('invalid')

        // Check if we're dealing with an expired link.
        } else if (response.data === 'expired') {
          throw new Error('expired')

        // Otherwise, extract the data from the response to populate the form.
        } else { this.form = JSON.parse(response.data) }

      // If we cannot load the form, we should just go tell the user that we
      // cannot find the form.
      } catch (error) {
        // Redirect to 404 in case of an invalid error.
        if (error.message === 'invalid') {
          this.$nuxt.error({
            statusCode: 404,
            message: 'This form could not be found.'
          })

        // Redirect to 498 in case of an expired link.
        } else if (error.message === 'expired') {
          this.$nuxt.error({
            statusCode: 498,
            message: 'This link has expired.'
          })
        }
      }
    },
    // Method to send a response with the current form submission.
    async respond () {
      // Send the response.
      const response = await this.$axios.post('forms/response/', {
        form: this.form.id,
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
