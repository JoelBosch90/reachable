<template>
  <v-form
    ref="form"
    v-model="valid"
    @submit.prevent="onSubmit"
  >
    <v-container>
      <slot />
    </v-container>
    <v-card-actions>
      <v-btn
        type="submit"
        color="success"
        :disabled="!valid"
        @click="validate"
      >
        Submit
      </v-btn>
    </v-card-actions>
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
      valid: false
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
    }
  }
}
</script>
