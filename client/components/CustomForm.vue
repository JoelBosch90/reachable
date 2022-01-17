<template>
  <Form
    ref="form"
    v-model="form"
    @submit="createLink"
  >
    <FormInput
      v-model="form.name"
      :label="inputs.name.label"
      :required="inputs.name.required"
      :rules="inputs.name.rules"
      :hint="inputs.name.hint"
    />
    <FormInput
      v-model="form.description"
      :label="inputs.description.label"
      :required="inputs.description.required"
      :rules="inputs.description.rules"
      :hint="inputs.description.hint"
    />
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
        name: '',
        description: '',
        email: ''
      },
      inputs: {
        name: {
          label: 'Name',
          rules: [
            value => !!value || 'Please name your form.'
          ],
          hint: 'This name is used in the form and in your UI.',
          required: true
        },
        description: {
          label: 'Description',
          rules: [],
          hint: 'This description will be shown near your form. You can use' +
                ' this to explain the form\'s purpose or ask questions to' +
                ' your respondents.',
          required: false
        },
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
          hint: 'Any responses to this form will be sent to this email' +
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
