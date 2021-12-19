<template>
  <v-card
    width="50%"
    class="mx-auto mt-5"
  >
    <v-card-title>
      <h1 class="display-1">
        {{ form.name }}
      </h1>
    </v-card-title>
    <v-card-text
      v-if="!responded"
    >
      <p>
        {{ form.description }}
      </p>
      <GenericForm
        ref="form"
        v-model="form"
        @submit="respond"
      >
        <GenericFormInput
          v-for="input in form.inputs"
          :key="input.name"
          v-model="response[input.name]"
          :label="input.name"
          :hint="input.title"
          :required="true"
        />
      </GenericForm>
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
        inputs: [],
        error: ''
      },
      // This is the input that the user has added to the form.
      response: {},
      responded: false
    }
  },
  mounted () {
    // Immediately load the form.
    this.load()
  },
  methods: {
    // Method to load the form from from the server.
    async load () {
      // Get the information about the form.
      const response = await this.$axios.get('forms/link/' + this.$route.params.key)

      // Extract the data from the response.
      this.form = JSON.parse(response.data)
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
      if (response) {
        this.responded = true

      // If we didn't get a valid response, something went wrong server-side. We
      // should tell the user that something has gone wrong.
      } else {
        this.$refs.form.showError('Error occurred: your response could not be sent.')
      }
    }
  }
}
</script>
