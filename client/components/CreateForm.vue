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
        ref="form"
        v-model="form"
        @submit="createLink"
      >
        <GenericFormInput
          v-model="form.name"
          :label="inputs.name.label"
          :required="inputs.name.required"
          :rules="inputs.name.rules"
          :hint="inputs.name.hint"
        />
        <GenericFormInput
          v-model="form.description"
          :label="inputs.description.label"
          :required="inputs.description.required"
          :rules="inputs.description.rules"
          :hint="inputs.description.hint"
        />
        <GenericFormInput
          v-model="form.email"
          :label="inputs.email.label"
          :required="inputs.email.required"
          :rules="inputs.email.rules"
          :hint="inputs.email.hint"
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
          hint: 'This description will be shown near your form. You can use this to explain the form\'s purpose or ask questions to your respondents.',
          required: false
        },
        email: {
          label: 'Email address',
          rules: [
            value => !!value || 'Please supply an email address to which we can send this form\'s responses.',
            // Use a simple regex to check for the presence of an @-symbol and a dot in the domain name.
            value => /.+@.+\..+/.test(value) || 'Please supply a valid email address.'
          ],
          hint: 'Any responses to this form will be sent to this email address.',
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
      const response = await this.$axios.post('forms/', this.form)

      // Make sure we have data, then redirect the user to the new form.
      if (response && response.data) {
        this.$router.push({
          name: 'form-key',
          params: {
            key: response.data
          }
        })
      // Otherwise, something has gone wrong and we should tell the user.
      } else { this.$refs.form.showError('Error occurred: your form could not be created.') }
    }
  }
}
</script>
