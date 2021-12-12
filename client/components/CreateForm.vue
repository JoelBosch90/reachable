<template>
  <v-card
    width="50%"
    class="mx-auto mt-5"
  >
    <v-card-title>
      <h1 class="display-1">
        Create new form
      </h1>
    </v-card-title>
    <v-card-text>
      <GenericForm
        v-model="form"
        @submit="createLink"
      >
        <GenericFormInput
          v-model="form.name"
          :label="'Name'"
          :required="true"
        />
        <GenericFormInput
          v-model="form.description"
          :label="'Description'"
          :required="false"
        />
        <GenericFormInput
          v-model="form.email"
          :label="'Email addresss'"
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
      form: {
        name: '',
        description: '',
        email: ''
      }
    }
  },
  methods: {
    // On submit, we want to attempt to create a new link with the information
    // submitted in the form.
    async createLink () {
      // Create the form, and get the key.
      const response = await this.$axios.post('forms/', this.form)

      // Redirect the user to the new form.
      this.$router.push({
        name: 'form-key',
        params: {
          key: response.data
        }
      })
    }
  }
}
</script>
