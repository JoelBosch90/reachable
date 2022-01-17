<template>
  <v-form
    ref="form"
    v-model="valid"
    @submit.prevent="onSubmit"
  >
    <p
      v-show="error"
      class="error--text"
    >
      {{ error }}
    </p>
    <slot />
    <v-btn
      type="submit"
      color="success"
      class="mt-4"
      :disabled="!valid"
      @click="validate"
    >
      {{ submit }}
    </v-btn>
  </v-form>
</template>

<script>
export default {
  props: {
    form: {
      type: Object,
      default: null
    },
    submit: {
      type: String,
      default: 'Submit'
    }
  },
  data () {
    return {
      // The form is invalid by default. We assume there should be some kind of
      // input for a useful form.
      valid: false,
      error: ''
    }
  },
  methods: {
    // Let the parent component handle submit events.
    onSubmit () {
      this.$emit('submit', this.form)
    },
    // Use Vuetify to validate the form.
    validate () {
      this.$refs.form.validate()
    },
    // Parent components can call this method to show an error message on the
    // form.
    showError (message) {
      // Are we given multiple errors to display? Display each one on a new
      // line.
      if (Array.isArray(message)) {
        this.error = message.join('\n')

      // Are we given a single error message?
      } else if (typeof message === 'string') {
        this.error = message

      // If we aren't given anything specific, we can display a generic error
      // message.
      } else {
        this.error = 'An unknown error has occurred.'
      }
    }
  }
}
</script>
