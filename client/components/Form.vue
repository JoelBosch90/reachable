<template>
  <v-form
    ref="form"
    v-model="valid"
    class="text"
    @submit.prevent="onSubmit"
  >
    <p
      v-if="error"
      class="body-1 error--text"
    >
      {{ error }}
    </p>
    <p
      v-else-if="formDisabled"
      class="body-1 error--text"
    >
      This form has been disabled and cannot currently be used.
    </p>
    <FormInput
      v-for="input in form.inputs"
      :key="input.name"
      v-model="responses[input.name]"
      :name="input.name"
      :label="input.label"
      :hint="input.hint"
      :required="input.required"
      :type="input.type"
      :rules="input.rules"
      :disabled="input.disabled || formDisabled"
    />
    <v-btn
      type="submit"
      color="success"
      class="mt-4"
      :disabled="!valid || formDisabled"
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
      responses: this.form.defaults || {},
      // The form is invalid by default. We assume there should be some kind of
      // input for a useful form.
      valid: false,
      error: ''
    }
  },
  computed: {
    formDisabled () {
      return this.form && this.form.disabled
    }
  },
  methods: {
    // Let the parent component handle submit events.
    onSubmit () {
      this.$emit('submit', this.responses)
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
