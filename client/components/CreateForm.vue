<template>
  <Form
    ref="form"
    :form="form"
    @submit="createLink"
  />
</template>

<script>
export default {
  props: {
    form: {
      type: Object,
      default () {
        return {
          disabled: true
        }
      }
    }
  },
  methods: {
    // On submit, we want to attempt to create a new link with the information
    // submitted in the form.
    async createLink (formData) {
      // Create the form, and get the key.
      const response = await this.$axios.post('forms/', formData)
        .catch((error) => {
          // Check if we have error response data.
          const data = error.response.data

          // Show a generic error message by default.
          let errorMessage = 'Error occurred: your form could not be created.'

          // Check if we're dealing if an error that is not field specific.
          if (data.non_field_errors) {
            errorMessage = data.non_field_errors
          }

          // Show the error message on the form.
          return this.$refs.form.showError(errorMessage)
        })

      // Make sure we have data, then throw the key up the event chain.
      if (response && response.data) {
        this.$emit('created', response.data)
      }
    }
  }
}
</script>
