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
    <v-card-text>
      <p>{{ form.description }}</p>
      <GenericForm
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
      response: {}
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

      // Extra the data from the response.
      const data = JSON.parse(response.data)

      // Load all data.
      this.form.description = data.description
      this.form.name = data.name
      this.form.id = data.id
      this.form.inputs = data.inputs
    },
    // Method to send a response with the current form submission.
    async respond () {
      // Send the response.
      await this.$axios.post('forms/response/', {
        form: this.form.id,
        inputs: this.response
      })
    }
  }
}
</script>
