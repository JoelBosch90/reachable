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
      Submit
    </v-btn>
  </v-form>
</template>

<script>
export default {
  props: {
    form: {
      type: Object,
      default: null
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
      this.error = message || 'An unknown error has occurred.'
    }
  }
}
</script>
