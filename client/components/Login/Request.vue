<template>
  <v-card>
    <v-card-title>
      <h1 class="display-1">
        Login via email link
      </h1>
    </v-card-title>
    <v-card-text
      v-if="requested"
    >
      Check your inbox for your login link!
    </v-card-text>
    <v-card-text
      v-else
    >
      <Form
        ref="form"
        v-model="form"
        @submit="requestLogin"
      >
        <FormInput
          v-model="form.email"
          :label="inputs.email.label"
          :required="inputs.email.required"
          :rules="inputs.email.rules"
          :hint="inputs.email.hint"
        />
      </Form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      form: {
        email: ''
      },
      inputs: {
        email: {
          label: 'Email address',
          rules: [
            value => !!value || 'Please supply an email address to which we can send a login link.',
            // Use a simple regex to check for the presence of an @-symbol and a dot in the domain name.
            value => /.+@.+\..+/.test(value) || 'Please supply a valid email address.'
          ],
          hint: 'We will send a link to your email address. You can login by simply clicking the link!',
          required: true
        }
      },
      requested: false
    }
  },
  methods: {
    // On submit, we want to request a login link.
    async requestLogin () {
      // Request the login link.
      const response = await this.$axios.post('login/', this.form)

      // Check that we've made a valid request.
      if (response && response.data) {
        this.request = true
      // Otherwise, something has gone wrong and we should tell the user.
      } else { this.$refs.form.showError('Error occurred: we could not send you a login link.') }
    }
  }
}
</script>
