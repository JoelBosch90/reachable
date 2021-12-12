<template>
  <v-app>
    <v-card>
      <h2>
        {{ name }}
      </h2>
      <p>
        {{ description }}
      </p>
      <Form-old :id="id" :fields="fields" />
    </v-card>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      name: '',
      id: 0,
      description: '',
      fields: []
    }
  },
  mounted () {
    // Immediately load the form.
    this.load()
  },
  methods: {
    // Method to load the from from the server.
    async load () {
      // Get the information about the form.
      const response = await this.$axios.get('forms/link/' + this.$route.params.key)

      // Extra the data from the response.
      const data = JSON.parse(response.data)

      // Load all data.
      this.description = data.description
      this.name = data.name
      this.id = data.id
      this.fields = data.inputs
    }
  }
}
</script>
