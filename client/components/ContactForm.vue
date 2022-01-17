<template>
  <Form
    ref="form"
    v-model="form"
    submit="Create form"
    @submit="createLink"
  >
    <FormInput
      v-model="form.email"
      :label="inputs.email.label"
      :required="inputs.email.required"
      :rules="inputs.email.rules"
      :hint="inputs.email.hint"
    />
  </Form>
</template>

<script>
export default {
  data () {
    return {
      form: {
        name: 'Contact me!',
        description: 'You can use the form below to contact me. Please' +
                     ' include your contact details if you want me to reach' +
                     ' back out to you!',
        email: ''
      },
      inputs: {
        email: {
          label: 'Email address',
          rules: [
            value => !!value || 'Please supply an email address to which we' +
                                ' can send this form\'s responses.',
            // Use a simple regex to check for the presence of an @-symbol and
            // a dot in the domain name.
            value => /.+@.+\..+/.test(value) || 'Please supply a valid email' +
                                                ' address.'
          ],
          hint: 'Any responses to the form will be sent to this email' +
                ' address.',
          required: true
        }
      }
    }
  },
  methods: {
    // On submit, we want to attempt to create a new link with the information
    // submitted in the form.
    async createLink () {
      // Create the form, and get the key.
      const response = await this.$axios.post('forms/', this.form).catch((error) => {
        // Check if we have error response data.
        const data = error.response.data

        // Check if we're dealing if an error that is not field specific.
        if (data.non_field_errors) {
          return this.$refs.form.showError(data.non_field_errors)

        // Otherwise, we have to give a generic error.
        } else {
          return this.$refs.form.showError('Error occurred: your form could' +
                                           ' not be created.')
        }
      })

      // Make sure we have data, then redirect the user to the new form.
      if (response && response.data) {
        this.$router.push({
          name: 'form-share-key',
          params: {
            key: response.data
          }
        })
      }
    }
  }
}
</script>
